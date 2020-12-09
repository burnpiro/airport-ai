import Layout from "../Layout/Layout";

import "./App.css";
import Simulation from "../Simulation/Simulation";
import { useReducer } from "react";

const defaultState = {
  selectedMenu: [],
};

function reducer(state = defaultState, action) {
  switch (action.type) {
    case "selectMenu":
      return { ...state, selectedMenu: [...state.selectedMenu, action.value] };
    case "deselectMenu":
      return {
        ...state,
        selectedMenu: state.selectedMenu.filter(
          (item) => item !== action.value
        ),
      };
    default:
      return state;
  }
}

function App() {
  const [state, dispatch] = useReducer(
    reducer,
    defaultState,
    () => defaultState
  );

  const onMenuChange = (item) => {
    dispatch({
      type: state.selectedMenu.includes(item) ? "deselectMenu" : "selectMenu",
      value: item,
    });
  };

  return (
    <Layout onMenuChange={onMenuChange} selectedMenu={state.selectedMenu}>
      <Simulation
        settings={{ showLayers: state.selectedMenu.includes("layers") }}
      />
    </Layout>
  );
}

export default App;
