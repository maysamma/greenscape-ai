import { useState } from "react";
import { uploadFloorPlan } from "../services/uploadService";

export default function Upload() {
  const [projectName, setProjectName] = useState("");
  const [buildingType, setBuildingType] = useState("");
  const [location, setLocation] = useState("");
  const [orientation, setOrientation] = useState("");
  const [area, setArea] = useState("");
  const [file, setFile] = useState(null);

  async function handleSubmit(e) {

    e.preventDefault();

    const formData = new FormData();

    formData.append("project_name", projectName);
    formData.append("building_type", buildingType);
    formData.append("location", location);
    formData.append("orientation", orientation);
    formData.append("area", area);
    formData.append("file", file);

    try{

        const result = await uploadFloorPlan(formData);

        alert(
            `Project Uploaded Successfully

  Project ID:
  ${result.project_id}`
        );

        console.log(result);

    }

    catch(error){

        console.error(error);

        alert("Upload Failed");

    }

}

  return (
    <div style={{ maxWidth: "600px", margin: "50px auto" }}>
      <h1>GreenScape AI</h1>
      <h2>Upload Floor Plan</h2>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Project Name"
          value={projectName}
          onChange={(e) => setProjectName(e.target.value)}
        />
        <br /><br />

        <input
          type="text"
          placeholder="Building Type"
          value={buildingType}
          onChange={(e) => setBuildingType(e.target.value)}
        />
        <br /><br />

        <input
          type="text"
          placeholder="Location"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
        />
        <br /><br />

        <input
          type="text"
          placeholder="Orientation"
          value={orientation}
          onChange={(e) => setOrientation(e.target.value)}
        />
        <br /><br />

        <input
          type="number"
          placeholder="Area (m²)"
          value={area}
          onChange={(e) => setArea(e.target.value)}
        />
        <br /><br />

        <input
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
        />
        <br /><br />

        <button type="submit">
          Analyze Design
        </button>
      </form>
    </div>
  );
}