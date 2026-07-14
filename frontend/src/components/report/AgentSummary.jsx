import Card from "../common/Card";

const agents = [

  "Vision Agent",

  "Architecture Agent",

  "Energy Agent",

  "Lighting Agent",

  "Accessibility Agent",

  "Report Generator",

];

export default function AgentSummary() {

  return (

    <Card>

      <h2 className="text-2xl font-bold mb-6">

        AI Agents Summary

      </h2>

      <div className="space-y-4">

        {agents.map(agent => (

          <div
            key={agent}
            className="flex justify-between"
          >

            <span>{agent}</span>

            <span className="text-green-600 font-semibold">

              ✔ Completed

            </span>

          </div>

        ))}

      </div>

    </Card>

  );

}