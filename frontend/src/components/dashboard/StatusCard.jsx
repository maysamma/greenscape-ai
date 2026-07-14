import Card from "../common/Card";


export default function StatusCard({
  analysis,
}) {
  const agents = analysis?.agents || [];

  return (
    <Card>
      <h2 className="text-2xl font-bold mb-8">
        AI Agents Status
      </h2>

      <div className="space-y-5">
        {agents.length === 0 ? (
          <p className="text-slate-500">
            No agent status is available.
          </p>
        ) : (
          agents.map((agent) => (
            <div
              key={agent.name}
              className="flex justify-between items-center gap-4"
            >
              <span>
                {agent.name}
              </span>

              <span
                className={`
                  font-semibold
                  ${getStatusClass(agent.status)}
                `}
              >
                ● {agent.status}
              </span>
            </div>
          ))
        )}
      </div>
    </Card>
  );
}


function getStatusClass(status) {
  switch (status) {
    case "Completed":
      return "text-green-600";

    case "Running":
      return "text-blue-600";

    case "Failed":
      return "text-red-600";

    default:
      return "text-slate-400";
  }
}