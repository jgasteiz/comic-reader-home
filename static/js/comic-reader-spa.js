(function () {
  "use strict";

  var h = React.createElement;
  var useState = React.useState;
  var useEffect = React.useEffect;
  var useCallback = React.useCallback;
  var useRef = React.useRef;

  var data = window.__COMIC_DATA__;
  var PREFETCH_AHEAD = 5;

  function pageUrl(page) {
    return data.pageSrcBaseUrl + page + "/";
  }

  function prefetchPages(center, cache) {
    // Next pages first, then previous pages
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

  function ComicReader() {
    var pageState = useState(data.initialPage);
    var currentPage = pageState[0];
    var setCurrentPage = pageState[1];

    var loadingState = useState(true);
    var isLoading = loadingState[0];
    var setIsLoading = loadingState[1];

    var initialZoom = Number(new URLSearchParams(window.location.search).get("width")) || 100;
    var zoomState = useState(initialZoom);
    var zoomPct = zoomState[0];
    var setZoomPct = zoomState[1];

    // Persistent cache of prefetched Image objects, keyed by page number
    var cacheRef = useRef({});
    var imageAreaRef = useRef(null);

    // Scroll to top, update URL, and prefetch surrounding pages whenever currentPage changes
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

    // Sync width to URL
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

    var goToPage = useCallback(
      function (page) {
        if (page < 0 || page >= data.numPages) return;
        setIsLoading(true);
        setCurrentPage(page);

        // Fire-and-forget progress update
        fetch(data.progressUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ page_number: page }),
        }).catch(function () {});
      },
      []
    );

    // Keyboard navigation
    useEffect(function () {
      function onKeyDown(e) {
        if (e.key === "ArrowRight" || e.key === " ") {
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

    function onContainerClick(e) {
      var rect = e.currentTarget.getBoundingClientRect();
      var x = e.clientX - rect.left;
      var pct = x / rect.width;
      if (pct >= 0.8) {
        goToPage(currentPage + 1);
      } else if (pct <= 0.2) {
        goToPage(currentPage - 1);
      }
    }

    var imgSrc = pageUrl(currentPage);

    // Styles
    var containerStyle = {
      display: "flex",
      flexDirection: "column",
      height: "100vh",
      background: "#000",
    };

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

    var selectStyle = {
      background: "#333",
      color: "#fff",
      border: "1px solid #555",
      borderRadius: "4px",
      padding: "4px 8px",
      fontSize: "14px",
      marginRight: "8px",
    };

    var pageOptions = [];
    for (var p = 0; p < data.numPages; p++) {
      pageOptions.push(
        h("option", { key: p, value: p }, "Page " + (p + 1))
      );
    }

    var ZOOM_OPTIONS = [100, 90, 80, 70, 60];
    var zoomOptions = ZOOM_OPTIONS.map(function (pct) {
      return h("option", { key: pct, value: pct }, pct + "%");
    });

    return h("div", { style: containerStyle }, [
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
      h("div", { key: "bottom-bar", style: bottomBarStyle }, [
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
        h(
          "a",
          {
            key: "exit",
            href: data.parentDirectoryUrl + "#" + data.comicId,
            style: exitLinkStyle,
          },
          "\u2715"
        ),
      ]),
    ]);
  }

  var root = ReactDOM.createRoot(document.getElementById("comic-reader-root"));
  root.render(h(ComicReader));
})();
