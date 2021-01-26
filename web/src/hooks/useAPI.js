import {useEffect, useMemo, useRef, useState} from "react";
import useWebSocket, {ReadyState} from "react-use-websocket";
import useInterval from "./useInterval";

function useAPI(
  socketURI = "ws://localhost:8081",
  { mockDataURI, onConnectionStatusChange, interval = 30 }
) {
  const [socketUrl] = useState(socketURI);
  const [shouldUseMock, setShouldUseMock] = useState(false);
  const [mockData, setMockData] = useState([]);
  const [count, setCount] = useState(0);

  useInterval(() => {
    setCount(count + 1 > mockData.length ? 0 : count + 1);
  }, 500);

  const { lastMessage, readyState } = useWebSocket(socketUrl);

  const connectionStatus = {
    [ReadyState.CONNECTING]: "Connecting",
    [ReadyState.OPEN]: "Open",
    [ReadyState.CLOSING]: "Closing",
    [ReadyState.CLOSED]: "Closed",
    [ReadyState.UNINSTANTIATED]: "Uninstantiated",
  }[readyState];

  useEffect(() => {
    if (typeof onConnectionStatusChange === "function") {
      onConnectionStatusChange(connectionStatus);
    }
    setShouldUseMock(connectionStatus === "Closed");
    // eslint-disable-next-line
  }, [connectionStatus]);

  useEffect(() => {
    if (shouldUseMock && mockData.length === 0) {
      const fetchData = async () => {
        try {
          let result = await fetch(mockDataURI);
          result = await result.json();
          setMockData(result);
        } catch (error) {
          console.error(
            "There was an error when fetching mocked data at " + mockData
          );
        }
      };

      fetchData();
    }
  }, [shouldUseMock, mockData, mockDataURI]);

  useEffect(() => {
    setCount(0)
  }, [mockData]);

  if (shouldUseMock) {
    return {listOfObjects: mockData[count] || {}}
  }
  return { listOfObjects: JSON.parse(
      lastMessage && lastMessage.data && typeof lastMessage.data === "string"
        ? lastMessage.data
        : '{ "passengers": [], "flights": [], "gates": [] }'
    ) };
}

export default useAPI;
