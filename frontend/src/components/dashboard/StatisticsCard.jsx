import Card from "../common/Card";



export default function StatisticsCard({ analysis }) {

  const statistics = [
    {
      title: "Overall Score",
      score: analysis.overall_score,
    },
    {
      title: "Architecture",
      score: analysis.scores.architecture,
    },
    {
      title: "Sustainability",
      score: analysis.scores.sustainability,
    },
    {
      title: "Energy",
      score: analysis.scores.energy,
    },
    {
      title: "Lighting",
      score: analysis.scores.lighting,
    },
  ];

  return (
    <Card>

      <h2 className="text-2xl font-bold mb-8">
        Analysis Results
      </h2>

      <div className="space-y-5">

        {statistics.map((item) => (

          <div key={item.title}>

            <div className="flex justify-between mb-2">

              <span>{item.title}</span>

              <span className="font-bold text-green-600">
                {item.score}%
              </span>

            </div>

            <div className="h-3 bg-slate-200 rounded-full">

              <div
                className="bg-green-600 h-3 rounded-full"
                style={{
                  width: `${item.score}%`,
                }}
              />

            </div>

          </div>

        ))}

      </div>

    </Card>
  );
}