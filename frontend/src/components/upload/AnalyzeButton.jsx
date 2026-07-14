import { Brain } from "lucide-react";

import Button from "../common/Button";


export default function AnalyzeButton({
  loading,
  onAnalyze,
}) {
  return (
    <div className="text-center mt-12">
      <Button
        type="button"
        onClick={onAnalyze}
        disabled={loading}
        className="
          bg-green-600
          hover:bg-green-700
          disabled:bg-slate-400
          disabled:cursor-not-allowed
          text-white
          px-10
          py-4
          inline-flex
          items-center
          gap-3
        "
      >
        <Brain size={22} />

        {loading
          ? "Analyzing..."
          : "Start AI Analysis"}
      </Button>
    </div>
  );
}