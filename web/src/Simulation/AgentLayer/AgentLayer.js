import {
  Fragment,
  useState,
  useMemo,
  useRef,
  useEffect,
} from "react";
import useWebSocket, { ReadyState } from "react-use-websocket";
import Agent from "../Agent/Agent";
import generateAgents from "../../helpers/generateAgents";

export const AgentLayer = ({ onConnectionStatusChange }) => {
  const [socketUrl] = useState("ws://localhost:8081");
  const messageHistory = useRef([]);

  const { lastMessage, readyState } = useWebSocket(socketUrl);

  messageHistory.current = useMemo(
    () => messageHistory.current.concat(lastMessage),
    [lastMessage]
  );

  // const handleClickSendMessage = useCallback(() => sendMessage("Hello"), []);

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
  }, [connectionStatus, onConnectionStatusChange]);

  const listOfAgents =
    JSON.parse(lastMessage && lastMessage.data &&
      typeof lastMessage.data === "string" ?  lastMessage.data : '{ "passengers": [] }');

  const agents = generateAgents(listOfAgents.passengers || []).map((data, id) => {
    return (
      <Agent
        position={data.position}
        size={data.size}
        key={data.id}
        styles={data.style}
      />
    );
  });
  return (
    <Fragment>
      {/*<button*/}
      {/*  onClick={handleClickSendMessage}*/}
      {/*  disabled={readyState !== ReadyState.OPEN}*/}
      {/*>*/}
      {/*  Click Me to send 'Hello'*/}
      {/*</button>*/}
      {agents}
      {/*<Agent styles={{*/}
      {/*  color: 'black',*/}
      {/*  stroke: 'black',*/}
      {/*  strokeWidth: 2,*/}
      {/*}} size={40} position={{x: 700, y: 500}} />*/}
    </Fragment>
  );
};
