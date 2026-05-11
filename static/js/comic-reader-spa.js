// Comic Reader SPA.
//
// Renders a single comic as a full-page React app: the current page's
// image, a bottom bar with page/zoom controls, and a fullscreen toggle.
// Surrounding pages are prefetched as the reader navigates, the current
// page and zoom are mirrored in the URL, and progress is POSTed back to
// the server on every navigation.
//
// Data comes from `window.__COMIC_DATA__`, which the Django template
// injects (URLs, page count, initial page, comic id, etc.).

(function () {
  "use strict";

  // ---------------------------------------------------------------
  // React shorthands
  //
  // React and ReactDOM are loaded as globals via <script> tags; this
  // file is plain ES5 so it can run without a build step.
  // ---------------------------------------------------------------

  var h = React.createElement;
  var useState = React.useState;
  var useEffect = React.useEffect;
  var useCallback = React.useCallback;
  var useRef = React.useRef;

  // ---------------------------------------------------------------
  // Module-level data and tunables
  // ---------------------------------------------------------------

  // Server-injected blob with everything the SPA needs to render and
  // talk back to the backend.
  var data = window.__COMIC_DATA__;

  // How many pages to warm in each direction around the current one.
  // Higher = smoother but more bandwidth/memory.
  var PREFETCH_AHEAD = 5;

  // ---------------------------------------------------------------
  // Helpers
  // ---------------------------------------------------------------

  // Build the URL for a given page number.
  function pageUrl(page) {
    return data.pageSrcBaseUrl + page + "/";
  }

  // Warm the browser cache with images for the pages around `center`,
  // so the next/previous page tends to render instantly. Image objects
  // are kept in `cache` so the references survive long enough for the
  // browser to actually treat them as hits when React asks for them.
  function prefetchPages(center, cache) {
    // Pages ahead are more likely to be the next one viewed, so they
    // go first in the queue.
    var toFetch = [];
    var i;
    for (i = 1; i <= PREFETCH_AHEAD; i++) {
      var next = center + i;
      if (next < data.numPages && !cache[next]) toFetch.push(next);
    }
    for (i = 1; i <= PREFETCH_AHEAD; i++) {
      var prev = center - i;
      if (prev >= 0 && !cache[prev]) toFetch.push(prev);
    }
    toFetch.forEach(function (page) {
      var img = new Image();
      img.src = pageUrl(page);
      cache[page] = img;
    });
  }

  // ---------------------------------------------------------------
  // ComicReader component
  // ---------------------------------------------------------------

  function ComicReader() {
    // ---- State ----------------------------------------------------

    // Zero-based index of the page currently displayed.
    var pageState = useState(data.initialPage);
    var currentPage = pageState[0];
    var setCurrentPage = pageState[1];

    // True while the current page's image is still loading.
    var loadingState = useState(true);
    var isLoading = loadingState[0];
    var setIsLoading = loadingState[1];

    // Image width as a percent of the image area. Read from the URL so
    // a refresh/share preserves the user's chosen zoom.
    var initialZoom = Number(new URLSearchParams(window.location.search).get("width")) || 100;
    var zoomState = useState(initialZoom);
    var zoomPct = zoomState[0];
    var setZoomPct = zoomState[1];

    // Mirrors the browser's fullscreen state. Kept in sync via the
    // fullscreenchange listener so ESC / swipe-down updates the UI too.
    var fullscreenState = useState(false);
    var isFullscreen = fullscreenState[0];
    var setIsFullscreen = fullscreenState[1];

    // Whether the bottom bar is on screen. Auto-hidden on entering
    // fullscreen and toggleable with a tap in the middle of the page.
    var barState = useState(true);
    var isBarVisible = barState[0];
    var setIsBarVisible = barState[1];

    // ---- Refs -----------------------------------------------------

    // Persistent { pageNumber -> Image } map for prefetched pages.
    var cacheRef = useRef({});
    // The scrollable image area; reset to top on each page change.
    var imageAreaRef = useRef(null);
    // The element passed to requestFullscreen — i.e. the whole reader.
    var containerRef = useRef(null);

    // ---- Effects --------------------------------------------------

    // On page change: scroll to top, mirror page in the URL, and
    // prefetch neighbouring pages.
    useEffect(
      function () {
        if (imageAreaRef.current) {
          imageAreaRef.current.scrollTop = 0;
        }
        var url = new URL(window.location);
        url.searchParams.set("page_number", currentPage);
        window.history.replaceState(null, "", url);
        prefetchPages(currentPage, cacheRef.current);
      },
      [currentPage]
    );

    // Mirror zoom in the URL. 100% is the implicit default and is left
    // out of the URL to keep links clean.
    useEffect(
      function () {
        var url = new URL(window.location);
        if (zoomPct === 100) {
          url.searchParams.delete("width");
        } else {
          url.searchParams.set("width", zoomPct);
        }
        window.history.replaceState(null, "", url);
      },
      [zoomPct]
    );

    // Keep our isFullscreen state in sync with the browser, including
    // exits the user triggers outside our toggle (ESC, swipe-down, the
    // browser's own fullscreen UI). Also auto-restores the bottom bar
    // on exit so controls don't get stranded off-screen.
    useEffect(function () {
      function onChange() {
        var el =
          document.fullscreenElement || document.webkitFullscreenElement;
        var active = !!el;
        setIsFullscreen(active);
        setIsBarVisible(!active);
      }
      document.addEventListener("fullscreenchange", onChange);
      document.addEventListener("webkitfullscreenchange", onChange);
      return function () {
        document.removeEventListener("fullscreenchange", onChange);
        document.removeEventListener("webkitfullscreenchange", onChange);
      };
    }, []);

    // Keyboard navigation: left/right arrows turn pages, up/down arrows
    // scroll the current page by 15% of the viewport, space snaps
    // through scroll stops on the current page, ESC leaves the reader
    // and jumps back to this comic's row in the parent listing.
    useEffect(function () {
      function onKeyDown(e) {
        if (e.key === "ArrowRight") {
          e.preventDefault();
          setCurrentPage(function (prev) {
            var next = prev + 1;
            if (next >= data.numPages) return prev;
            setIsLoading(true);
            fetch(data.progressUrl, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ page_number: next }),
            }).catch(function () {});
            return next;
          });
        } else if (e.key === " ") {
          e.preventDefault();
          var area = imageAreaRef.current;
          if (area) {
            // Snap through a fixed set of stops so the user always
            // reaches the bottom of the page in a predictable number
            // of presses: 1 when most of the page already fits on
            // screen, 2 otherwise (top -> middle -> bottom).
            var maxScroll = area.scrollHeight - area.clientHeight;
            if (maxScroll > 0) {
              var stops =
                area.clientHeight / area.scrollHeight > 0.5
                  ? [0, maxScroll]
                  : [0, maxScroll / 2, maxScroll];
              var target = maxScroll;
              for (var s = 0; s < stops.length; s++) {
                if (stops[s] > area.scrollTop + 1) {
                  target = stops[s];
                  break;
                }
              }
              area.scrollTo({ top: target, behavior: "smooth" });
            }
          }
        } else if (e.key === "ArrowLeft") {
          e.preventDefault();
          setCurrentPage(function (prev) {
            var next = prev - 1;
            if (next < 0) return prev;
            setIsLoading(true);
            fetch(data.progressUrl, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ page_number: next }),
            }).catch(function () {});
            return next;
          });
        } else if (e.key === "ArrowDown" || e.key === "ArrowUp") {
          e.preventDefault();
          var scrollArea = imageAreaRef.current;
          if (scrollArea) {
            var delta = scrollArea.clientHeight * 0.15;
            scrollArea.scrollBy({
              top: e.key === "ArrowDown" ? delta : -delta,
              behavior: "smooth",
            });
          }
        } else if (e.key === "Escape") {
          window.location.href =
            data.parentDirectoryUrl + "#" + data.comicId;
        }
      }
      document.addEventListener("keydown", onKeyDown);
      return function () {
        document.removeEventListener("keydown", onKeyDown);
      };
    }, []);

    // ---- Handlers -------------------------------------------------

    // Move to a specific page and report progress. No-op for out-of-
    // range pages so callers don't need to bounds-check.
    var goToPage = useCallback(
      function (page) {
        if (page < 0 || page >= data.numPages) return;
        setIsLoading(true);
        setCurrentPage(page);

        // Fire-and-forget — the UI doesn't need to wait on this.
        fetch(data.progressUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ page_number: page }),
        }).catch(function () {});
      },
      []
    );

    // Tap zones across the image area:
    //   left 20%  -> previous page
    //   right 20% -> next page
    //   middle 60% -> toggle the bottom bar
    // The narrow side zones avoid accidental page flips when tapping
    // near the centre of the image.
    function onContainerClick(e) {
      var rect = e.currentTarget.getBoundingClientRect();
      var x = e.clientX - rect.left;
      var pct = x / rect.width;
      if (pct >= 0.8) {
        goToPage(currentPage + 1);
      } else if (pct <= 0.2) {
        goToPage(currentPage - 1);
      } else {
        setIsBarVisible(function (v) {
          return !v;
        });
      }
    }

    // Toggle browser fullscreen on the reader container. Falls back to
    // documentElement if the ref isn't attached yet, and uses webkit-
    // prefixed APIs on Safari. Note: iPhone Safari does not support
    // fullscreen for non-video elements; PWA install is the workaround.
    var toggleFullscreen = useCallback(function () {
      var el = containerRef.current || document.documentElement;
      var inFullscreen =
        document.fullscreenElement || document.webkitFullscreenElement;
      if (inFullscreen) {
        var exit =
          document.exitFullscreen || document.webkitExitFullscreen;
        if (exit) exit.call(document);
      } else {
        var request =
          el.requestFullscreen || el.webkitRequestFullscreen;
        if (request) request.call(el);
      }
    }, []);

    // ---- Render ---------------------------------------------------

    var imgSrc = pageUrl(currentPage);

    // Styles. Inline objects keep this file dependency-free at the
    // cost of not being shareable across components — fine for a
    // single-component SPA.

    // Reader root: column layout filling the viewport. 100dvh tracks
    // the dynamic viewport on mobile so the bottom bar stays visible
    // when the address bar is showing.
    var containerStyle = {
      display: "flex",
      flexDirection: "column",
      height: "100dvh",
      background: "#000",
    };

    // Scrolling area that holds the page image; takes up all space
    // not used by the bottom bar.
    var imageAreaStyle = {
      flex: 1,
      display: "flex",
      justifyContent: "center",
      alignItems: "flex-start",
      overflowY: "auto",
      cursor: "pointer",
      position: "relative",
    };

    var imgStyle = {
      width: zoomPct + "%",
      maxWidth: "100%",
    };

    var loadingStyle = {
      position: "absolute",
      top: "50%",
      left: "50%",
      transform: "translate(-50%, -50%)",
      color: "#fff",
      fontSize: "18px",
    };

    var bottomBarStyle = {
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      padding: "8px 16px",
      background: "#111",
      color: "#fff",
      fontSize: "14px",
      flexShrink: 0,
    };

    var exitLinkStyle = {
      color: "#fff",
      textDecoration: "none",
      fontSize: "20px",
      lineHeight: 1,
    };

    var iconButtonStyle = {
      background: "transparent",
      border: "none",
      color: "#fff",
      fontSize: "20px",
      lineHeight: 1,
      cursor: "pointer",
      padding: "0 8px",
    };

    var rightControlsStyle = {
      display: "flex",
      alignItems: "center",
      gap: "8px",
    };

    var selectStyle = {
      background: "#333",
      color: "#fff",
      border: "1px solid #555",
      borderRadius: "4px",
      padding: "4px 8px",
      fontSize: "14px",
      marginRight: "8px",
    };

    // Pre-build the page <option>s once per render. Cheap relative to
    // the image work happening alongside it.
    var pageOptions = [];
    for (var p = 0; p < data.numPages; p++) {
      pageOptions.push(
        h("option", { key: p, value: p }, "Page " + (p + 1))
      );
    }

    // Width presets exposed in the zoom dropdown.
    var ZOOM_OPTIONS = [100, 90, 80, 70, 60];
    var zoomOptions = ZOOM_OPTIONS.map(function (pct) {
      return h("option", { key: pct, value: pct }, pct + "%");
    });

    return h("div", { ref: containerRef, style: containerStyle }, [
      // Image area: the page itself plus a centred "Loading..." overlay
      // while the next image is in flight.
      h(
        "div",
        { key: "image-area", ref: imageAreaRef, style: imageAreaStyle, onClick: onContainerClick },
        [
          isLoading
            ? h("div", { key: "loading", style: loadingStyle }, "Loading...")
            : null,
          h("img", {
            key: "page-img",
            src: imgSrc,
            style: imgStyle,
            onLoad: function () {
              setIsLoading(false);
            },
          }),
        ]
      ),
      // Bottom bar: page picker + indicator + zoom on the left,
      // fullscreen toggle and exit link on the right. Hidden when
      // `isBarVisible` is false (e.g. while in fullscreen).
      isBarVisible
        ? h("div", { key: "bottom-bar", style: bottomBarStyle }, [
            h("span", { key: "controls", style: { display: "flex", alignItems: "center" } }, [
              h(
                "select",
                {
                  key: "page-select",
                  value: currentPage,
                  onChange: function (e) {
                    goToPage(Number(e.target.value));
                  },
                  style: selectStyle,
                },
                pageOptions
              ),
              h("span", { key: "indicator", style: { marginRight: "12px" } }, currentPage + 1 + " / " + data.numPages),
              h(
                "select",
                {
                  key: "zoom-select",
                  value: zoomPct,
                  onChange: function (e) {
                    setZoomPct(Number(e.target.value));
                  },
                  style: selectStyle,
                },
                zoomOptions
              ),
            ]),
            h("span", { key: "right-controls", style: rightControlsStyle }, [
              h(
                "button",
                {
                  key: "fullscreen",
                  type: "button",
                  onClick: toggleFullscreen,
                  style: iconButtonStyle,
                  "aria-label": isFullscreen ? "Exit fullscreen" : "Enter fullscreen",
                },
                isFullscreen ? "⤢" : "⛶"
              ),
              h(
                "a",
                {
                  key: "exit",
                  href: data.parentDirectoryUrl + "#" + data.comicId,
                  style: exitLinkStyle,
                },
                "✕"
              ),
            ]),
          ])
        : null,
    ]);
  }

  // ---------------------------------------------------------------
  // Mount
  // ---------------------------------------------------------------

  var root = ReactDOM.createRoot(document.getElementById("comic-reader-root"));
  root.render(h(ComicReader));
})();
