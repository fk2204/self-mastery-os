// =============================================================================
// Self-Mastery OS — Service Worker
// =============================================================================
// Provides offline-first PWA support with tiered caching strategies.
//
// Static assets are precached on install and served cache-first.
// Dynamic assets (fonts, knowledge base JSONs) are cached on first fetch
// using strategy-appropriate routing.
// Navigation requests use stale-while-revalidate so the app loads instantly
// from cache while silently updating in the background.
// =============================================================================

const CACHE_VERSION = 'v1';
const STATIC_CACHE = `mastermind-static-${CACHE_VERSION}`;
const DYNAMIC_CACHE = `mastermind-dynamic-${CACHE_VERSION}`;

// Assets to precache during the install event.
// These form the minimal "app shell" needed to boot offline.
const PRECACHE_URLS = [
  '/dashboard.html',
  '/data/masters-data.js',
  '/manifest.json',
  '/icons/icon-192.svg',
  '/icons/icon-512.svg'
];

// ---------------------------------------------------------------------------
// Install — precache static assets and activate immediately
// ---------------------------------------------------------------------------
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then((cache) => {
        return cache.addAll(PRECACHE_URLS);
      })
      .then(() => {
        // Skip the waiting phase so the new SW activates immediately.
        return self.skipWaiting();
      })
  );
});

// ---------------------------------------------------------------------------
// Activate — purge stale caches and take control of all open clients
// ---------------------------------------------------------------------------
self.addEventListener('activate', (event) => {
  const EXPECTED_CACHES = new Set([STATIC_CACHE, DYNAMIC_CACHE]);

  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames
            .filter((name) => !EXPECTED_CACHES.has(name))
            .map((name) => {
              // Delete any cache that doesn't match the current version.
              return caches.delete(name);
            })
        );
      })
      .then(() => {
        // Claim all open clients so the new SW controls them right away
        // without requiring a page reload.
        return self.clients.claim();
      })
      .then(() => {
        // Notify all clients that the service worker has been updated.
        return self.clients.matchAll().then((clients) => {
          clients.forEach((client) => {
            client.postMessage({ type: 'SW_UPDATED' });
          });
        });
      })
  );
});

// ---------------------------------------------------------------------------
// Fetch — route requests to the appropriate caching strategy
// ---------------------------------------------------------------------------
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Only handle GET requests. Let POST/PUT/DELETE pass through to the network.
  if (request.method !== 'GET') {
    return;
  }

  // 1. Navigation requests (HTML pages)
  //    Strategy: Stale-while-revalidate
  //    Return the cached version immediately for instant load, then fetch a
  //    fresh copy from the network and update the cache in the background.
  //    If nothing is cached and the network fails, fall back to the cached
  //    dashboard.html (since this is an SPA, any route can be served by it).
  if (request.mode === 'navigate') {
    event.respondWith(handleNavigationRequest(request));
    return;
  }

  // 2. Google Fonts (CSS from googleapis.com, font files from gstatic.com)
  //    Strategy: Cache-first
  //    Font files are immutable (content-addressed URLs), so once cached
  //    they never need to be re-fetched.
  if (url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com') {
    event.respondWith(cacheFirst(request, DYNAMIC_CACHE));
    return;
  }

  // 3. Knowledge base JSON files (loaded dynamically by the wisdom engine)
  //    Strategy: Network-first with cache fallback
  //    These files may be updated between versions, so prefer fresh data,
  //    but serve the cached copy if the network is unavailable.
  if (url.pathname.startsWith('/knowledge_base/')) {
    event.respondWith(networkFirst(request, DYNAMIC_CACHE));
    return;
  }

  // 4. Static assets (JS, CSS, SVGs, JSON in /data/)
  //    Strategy: Cache-first with network fallback
  //    These are precached or versioned, so the cache is authoritative.
  if (isStaticAsset(url)) {
    event.respondWith(cacheFirst(request, STATIC_CACHE));
    return;
  }

  // 5. Everything else
  //    Strategy: Network-first with cache fallback
  //    For any other requests, try the network and fall back to cache.
  event.respondWith(networkFirst(request, DYNAMIC_CACHE));
});

// ---------------------------------------------------------------------------
// Strategy: Stale-while-revalidate (for navigation requests)
// ---------------------------------------------------------------------------
// Returns the cached response immediately (if available) while fetching a
// fresh version from the network to update the cache for the next load.
async function handleNavigationRequest(request) {
  try {
    const cache = await caches.open(STATIC_CACHE);
    const cachedResponse = await cache.match(request);

    // Fire off a network fetch to update the cache in the background.
    // We intentionally do NOT await this — the user gets the cached version
    // instantly, and the cache is silently refreshed.
    const networkUpdate = fetch(request)
      .then((networkResponse) => {
        if (networkResponse && networkResponse.ok) {
          cache.put(request, networkResponse.clone());
        }
        return networkResponse;
      })
      .catch(() => null);

    // If we have a cached version, return it immediately.
    if (cachedResponse) {
      return cachedResponse;
    }

    // No cache available — we must wait for the network.
    const networkResponse = await networkUpdate;
    if (networkResponse) {
      return networkResponse;
    }

    // Both cache and network failed — serve the cached SPA shell as a
    // fallback. Since dashboard.html is a single-page app, it can handle
    // any route client-side.
    return await offlineFallback();
  } catch (error) {
    return await offlineFallback();
  }
}

// ---------------------------------------------------------------------------
// Strategy: Cache-first with network fallback
// ---------------------------------------------------------------------------
// Best for immutable or versioned assets (fonts, static JS/CSS, icons).
// Checks the cache first; if not found, fetches from network and caches
// the response for future use.
async function cacheFirst(request, cacheName) {
  try {
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }

    const networkResponse = await fetch(request);
    if (networkResponse && networkResponse.ok) {
      try {
        const cache = await caches.open(cacheName);
        cache.put(request, networkResponse.clone());
      } catch (cacheError) {
        // Cache storage may be full or unavailable — still return the response.
      }
    }
    return networkResponse;
  } catch (error) {
    // Network failed and nothing in cache.
    return new Response('', { status: 408, statusText: 'Offline — resource not cached' });
  }
}

// ---------------------------------------------------------------------------
// Strategy: Network-first with cache fallback
// ---------------------------------------------------------------------------
// Best for data that may change (knowledge base JSONs, API calls).
// Tries the network first for fresh data; if that fails, falls back to
// whatever is cached.
async function networkFirst(request, cacheName) {
  try {
    const networkResponse = await fetch(request);
    if (networkResponse && networkResponse.ok) {
      try {
        const cache = await caches.open(cacheName);
        cache.put(request, networkResponse.clone());
      } catch (cacheError) {
        // Cache storage may be full — still return the network response.
      }
    }
    return networkResponse;
  } catch (error) {
    // Network unavailable — try the cache.
    try {
      const cachedResponse = await caches.match(request);
      if (cachedResponse) {
        return cachedResponse;
      }
    } catch (cacheError) {
      // Cache also failed.
    }
    return new Response('', { status: 408, statusText: 'Offline — resource not cached' });
  }
}

// ---------------------------------------------------------------------------
// Offline fallback — serve cached dashboard.html as the SPA shell
// ---------------------------------------------------------------------------
async function offlineFallback() {
  try {
    const cachedDashboard = await caches.match('/dashboard.html');
    if (cachedDashboard) {
      return cachedDashboard;
    }
  } catch (error) {
    // Cache unavailable.
  }

  // Last resort: return a minimal offline page.
  return new Response(
    '<!DOCTYPE html><html><head><meta charset="utf-8">' +
    '<meta name="viewport" content="width=device-width,initial-scale=1">' +
    '<title>Offline</title>' +
    '<style>body{background:#0a0a0f;color:#e0e0e0;font-family:system-ui,sans-serif;' +
    'display:flex;align-items:center;justify-content:center;min-height:100vh;margin:0;' +
    'text-align:center}h1{font-size:1.5rem;margin-bottom:0.5rem}p{color:#888;margin-top:0}</style>' +
    '</head><body><div><h1>You are offline</h1>' +
    '<p>Self-Mastery OS could not load. Connect to the internet and try again.</p>' +
    '</div></body></html>',
    { status: 503, headers: { 'Content-Type': 'text/html' } }
  );
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

// Determines whether a URL points to a static asset that should use
// cache-first strategy. Matches JS, CSS, SVG files and JSON files
// under the /data/ path.
function isStaticAsset(url) {
  const { pathname } = url;

  // JS, CSS, and SVG files
  if (/\.(js|css|svg)$/.test(pathname)) {
    return true;
  }

  // JSON files under /data/ (e.g., masters-data.js is already caught above,
  // but other data JSONs should also be cache-first)
  if (pathname.startsWith('/data/') && pathname.endsWith('.json')) {
    return true;
  }

  // The manifest.json at root
  if (pathname === '/manifest.json') {
    return true;
  }

  // Image files
  if (/\.(png|jpg|jpeg|gif|webp|ico)$/.test(pathname)) {
    return true;
  }

  return false;
}

// ---------------------------------------------------------------------------
// Message handler — allows clients to communicate with the SW
// ---------------------------------------------------------------------------
self.addEventListener('message', (event) => {
  if (event.data === 'skipWaiting') {
    self.skipWaiting();
  }
});
