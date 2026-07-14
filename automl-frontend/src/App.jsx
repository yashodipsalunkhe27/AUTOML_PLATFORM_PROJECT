import { BrowserRouter, Routes, Route } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Upload from "./pages/Upload";
import Analysis from "./pages/Analysis";
import Train from "./pages/Train";
import Results from "./pages/Results";
import Prediction from "./pages/Prediction";
import BatchPrediction from "./pages/BatchPrediction";
import History from "./pages/History";
import Reports from "./pages/Reports";
import Settings from "./pages/Settings";

function App() {
  return (
    <BrowserRouter>
      <Routes>

        <Route path="/" element={<Dashboard />} />

        <Route path="/upload" element={<Upload />} />

        <Route path="/analysis" element={<Analysis />} />

        <Route path="/train" element={<Train />} />

        <Route path="/results" element={<Results />} />

        <Route path="/prediction" element={<Prediction />} />

        <Route path="/batch" element={<BatchPrediction />} />

        <Route path="/reports" element={<Reports />} />

        <Route path="/history" element={<History />} />

        <Route path="/settings" element={<Settings />} />

      </Routes>
    </BrowserRouter>
  );
}

export default App;