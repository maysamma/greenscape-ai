import Button from "../common/Button";
import { Download } from "lucide-react";

export default function DownloadReport() {
  return (
    <div className="flex justify-center mt-10">
      <Button className="bg-green-600 hover:bg-green-700 text-white px-8 py-3 flex items-center gap-2">
        <Download size={20} />
        Download PDF Report
      </Button>
    </div>
  );
}