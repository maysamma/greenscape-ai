import Card from "../common/Card";
import { FileText } from "lucide-react";

export default function UploadCard({
  selectedFile,
}) {

  return (

    <Card className="mt-8">

      <h2 className="text-2xl font-bold mb-8">

        Uploaded File

      </h2>

      {!selectedFile && (

        <p className="text-slate-500">

          No file selected.

        </p>

      )}

      {selectedFile && (

        <div className="flex items-center gap-5">

          <div className="bg-green-100 p-5 rounded-xl">

            <FileText
              size={35}
              className="text-green-600"
            />

          </div>

          <div>

            <h3 className="font-semibold">

              {selectedFile.name}

            </h3>

            <p className="text-slate-500">

              {(selectedFile.size / 1024 / 1024).toFixed(2)} MB

            </p>

          </div>

        </div>

      )}

    </Card>

  );
}