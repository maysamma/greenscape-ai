import { useNavigate } from "react-router-dom";

import Container from "../components/common/Container";
import UploadForm from "../components/upload/UploadForm";
import FileDropzone from "../components/upload/FileDropzone";
import UploadCard from "../components/upload/UploadCard";
import AnalyzeButton from "../components/upload/AnalyzeButton";

import useUpload from "../hooks/useUpload";
import { uploadFloorPlan } from "../services/uploadService";
import { startAnalysis } from "../services/analysisService";


export default function Upload() {
  const navigate = useNavigate();

  const {
    selectedFile,
    setSelectedFile,

    projectInfo,
    setProjectInfo,

    loading,
    setLoading,

    setResult,
  } = useUpload();


  async function handleAnalyze() {
    if (!selectedFile) {
      alert("Please upload a floor plan first.");
      return;
    }

    if (
      !projectInfo.project_name?.trim() ||
      !projectInfo.building_type?.trim() ||
      !projectInfo.location?.trim()
    ) {
      alert("Please complete the project information.");
      return;
    }

    try {
      setLoading(true);

      // 1. Upload the floor plan and create the project.
      const uploadResponse = await uploadFloorPlan(
        selectedFile,
        projectInfo
      );

      console.log(
        "Upload response:",
        uploadResponse
      );

      const projectId =
        uploadResponse.project_id ??
        uploadResponse.id ??
        uploadResponse.project?.id;

      if (!projectId) {
        throw new Error(
          "The upload response does not contain project_id."
        );
      }

      setResult(uploadResponse);

      // 2. Start the real backend analysis.
      const analysisResponse = await startAnalysis(
        projectId
      );

      console.log(
        "Analysis start response:",
        analysisResponse
      );

      localStorage.setItem(
        "currentProjectId",
        projectId
      );

      // 3. Open the dashboard.
      navigate(
        `/dashboard/${projectId}`
      );

    } catch (error) {
      console.error(
        "Upload or analysis failed:",
        error
      );

      const message =
        error.response?.data?.detail ??
        error.message ??
        "Failed to start the analysis.";

      alert(message);

    } finally {
      setLoading(false);
    }
  }


  return (
    <section className="py-20">
      <Container>
        <h1 className="text-5xl font-bold">
          Upload Architectural Design
        </h1>

        <p className="text-slate-500 mt-4 mb-10">
          Upload your floor plan and let GreenScape AI analyze your design.
        </p>

        <UploadForm
          projectInfo={projectInfo}
          setProjectInfo={setProjectInfo}
        />

        <FileDropzone
          selectedFile={selectedFile}
          setSelectedFile={setSelectedFile}
        />

        <UploadCard
          selectedFile={selectedFile}
        />

        <AnalyzeButton
          loading={loading}
          onAnalyze={handleAnalyze}
        />
      </Container>
    </section>
  );
}