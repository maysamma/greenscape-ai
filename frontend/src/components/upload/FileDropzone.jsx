import { UploadCloud } from "lucide-react";
import Card from "../common/Card";

export default function FileDropzone({
  selectedFile,
  setSelectedFile,
}) {

  function handleFileChange(e) {

    const file = e.target.files[0];

    if (!file) return;

    setSelectedFile(file);
  }

  return (

    <Card className="mt-8">

      <label
        className="
        flex
        flex-col
        justify-center
        items-center
        h-80
        border-2
        border-dashed
        border-green-400
        rounded-2xl
        cursor-pointer
        hover:bg-green-50
        transition
        "
      >

        <UploadCloud
          size={60}
          className="text-green-600"
        />

        <h3 className="text-2xl font-bold mt-5">

          {selectedFile
            ? selectedFile.name
            : "Click to Upload"}

        </h3>

        <p className="text-slate-500 mt-3">

          PDF • PNG • JPG

        </p>

        <input
          type="file"
          accept=".pdf,.png,.jpg,.jpeg"
          onChange={handleFileChange}
          className="hidden"
        />

      </label>

    </Card>

  );
}