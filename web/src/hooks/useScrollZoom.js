import { useState, useEffect, useCallback } from "react";

const CTRL_KEY_IDX = 17;
const ZOOM_UP_LIMIT = 3.5;
const ZOOM_DOWN_LIMIT = 0.3;

function useScrollZoom(defaultZoom = 0.5) {
  const [scroll, setScroll] = useState(defaultZoom);
  const [currentKey, setCurrentKey] = useState(null);

  const handleUserKeyDown = useCallback((event) => {
    const { keyCode } = event;

    if (keyCode === CTRL_KEY_IDX) {
      setCurrentKey(keyCode);
    }
  }, []);

  const handleUserKeyUp = useCallback((event) => {
    setCurrentKey(null);
  }, []);

  const handleUserScroll = useCallback(
    (event) => {
      if (currentKey === CTRL_KEY_IDX) {
        event.preventDefault();
        const delta =
          (event.deltaY || -event.wheelDelta || event.detail) >> 10 || 1;
        const changedScroll =
          delta < 0 && scroll < ZOOM_UP_LIMIT
            ? scroll + 0.1
            : delta > 0 && scroll > ZOOM_DOWN_LIMIT
            ? scroll - 0.1
            : scroll;
        setScroll(changedScroll);
      }
    },
    [currentKey, scroll]
  );

  useEffect(() => {
    window.addEventListener("mousewheel", handleUserScroll, {
      passive: false,
      capture: true,
    });
    window.addEventListener("keydown", handleUserKeyDown);
    window.addEventListener("keyup", handleUserKeyUp);

    return () => {
      window.removeEventListener("mousewheel", handleUserScroll, {
        passive: false,
        capture: true,
      });
      window.removeEventListener("keydown", handleUserKeyDown);
      window.removeEventListener("keyup", handleUserKeyUp);
    };
  }, [handleUserScroll, handleUserKeyDown, handleUserKeyUp]);

  return scroll;
}

export default useScrollZoom;
