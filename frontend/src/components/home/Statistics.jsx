import { Brain, Leaf, Clock3, ClipboardCheck } from "lucide-react";
import Container from "../common/Container";

const stats = [
  {
    icon: Brain,
    value: "10+",
    title: "AI Agents",
  },
  {
    icon: Leaf,
    value: "95%",
    title: "Sustainability Accuracy",
  },
  {
    icon: ClipboardCheck,
    value: "8",
    title: "Review Categories",
  },
  {
    icon: Clock3,
    value: "<2 min",
    title: "Average Analysis",
  },
];

export default function Statistics() {
  return (
    <section className="py-20 bg-white">
      <Container>

        <div className="text-center mb-12">

          <h2 className="text-3xl font-bold">
            AI That Helps Architects Design Better
          </h2>

          <p className="text-slate-500 mt-3">
            Fast, intelligent and sustainability-focused architectural analysis.
          </p>

        </div>

        <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">

          {stats.map((item, index) => {

            const Icon = item.icon;

            return (

              <div
                key={index}
                className="rounded-2xl border border-slate-200 bg-slate-50 p-8 text-center hover:shadow-xl transition"
              >

                <div className="flex justify-center mb-5">

                  <div className="bg-green-100 p-4 rounded-full">

                    <Icon
                      size={28}
                      className="text-green-600"
                    />

                  </div>

                </div>

                <h3 className="text-4xl font-bold text-slate-800">

                  {item.value}

                </h3>

                <p className="mt-3 text-slate-500">

                  {item.title}

                </p>

              </div>

            );

          })}

        </div>

      </Container>
    </section>
  );
}