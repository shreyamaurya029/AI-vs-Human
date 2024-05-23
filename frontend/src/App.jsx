import { Routes, Route } from "react-router-dom";

import { Home, Error, Contributors } from "./Pages";

import { Navbar } from "./Components";

const App = () => {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="*" element={<Error />} />
        <Route path="/contributors" element={<Contributors />} />
      </Routes>
      {/* <Footer /> */}
    </>
  );
};

export default App;
