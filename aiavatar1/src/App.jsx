import "./App.css";
import SpeechUpload from "../pages/SpeechUpload";
import { Route, Routes, Router, BrowserRouter } from "react-router";
import TextUpload from "../pages/TextUpload";

function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/transcribe" element={<SpeechUpload />} />
          <Route path="/generate" element={<TextUpload />} />
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
