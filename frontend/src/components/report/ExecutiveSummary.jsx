import Card from "../common/Card";

export default function ExecutiveSummary() {
  return (
    <Card>

      <h2 className="text-2xl font-bold mb-6">
        Executive Summary
      </h2>

      <p className="leading-8 text-slate-600">

        GreenScape AI analyzed the uploaded architectural
        design and found excellent sustainability,
        accessibility and space utilization.

        Several improvements are recommended to enhance
        energy efficiency and natural ventilation.

      </p>

    </Card>
  );
}