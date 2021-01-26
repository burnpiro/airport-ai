import {Fragment, useEffect} from "react";
import Agent from "../Agent/Agent";
import generateAgents from "../../helpers/generateAgents";
import useAPI from "../../hooks/useAPI";

export const AgentLayer = ({ onConnectionStatusChange, onGatesChange }) => {
  const { listOfObjects: listOfAgents } = useAPI("ws://localhost:8081", {
    onConnectionStatusChange: onConnectionStatusChange,
    mockDataURI: "/airport-ai/out.json",
  });

  useEffect(() => {
    onGatesChange(listOfAgents.gates || []);
    // eslint-disable-next-line
  }, [listOfAgents.gates])

  const agents = generateAgents(listOfAgents.passengers || []).map(
    (data, id) => {
      return (
        <Agent
          position={data.position}
          size={data.size}
          key={data.id}
          styles={data.style}
        />
      );
    }
  );
  return <Fragment>{agents}</Fragment>;
};
