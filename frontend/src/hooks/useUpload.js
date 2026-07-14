import { useState } from "react";

export default function useUpload() {

  const [selectedFile, setSelectedFile] = useState(null);

  const [projectInfo, setProjectInfo] = useState({
    project_name: "",
    building_type: "Residential",
    location: "",
    orientation: "North",
    area: 0,
    floors: 1,
  });

  const [loading, setLoading] = useState(false);

  const [result, setResult] = useState(null);

  return {
    selectedFile,
    setSelectedFile,

    projectInfo,
    setProjectInfo,

    loading,
    setLoading,

    result,
    setResult,
  };

}