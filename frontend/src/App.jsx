import { Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import Upload from "./pages/Upload";
import Dashboard from "./pages/Dashboard";
import Report from "./pages/Report";
import NotFound from "./pages/NotFound";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />

      <Route path="/upload" element={<Upload />} />

      <Route path="/dashboard" element={<Dashboard />} />

      <Route path="/report" element={<Report />} />

      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}