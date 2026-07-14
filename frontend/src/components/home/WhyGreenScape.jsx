import {
  CheckCircle2,
  XCircle,
} from "lucide-react";

import Container from "../common/Container";
import SectionTitle from "../common/SectionTitle";

const traditional = [
  "Manual design review",
  "Multiple software tools",
  "Long analysis time",
  "Late sustainability review",
  "Higher redesign cost",
  "Subjective evaluation",
];

const greenscape = [
  "AI-powered analysis",
  "One integrated platform",
  "Results in minutes",
  "Early sustainability feedback",
  "Cost optimization suggestions",
  "Data-driven recommendations",
];

export default function WhyGreenScape() {
  return (
    <section className="py-24 bg-slate-50">

      <Container>

        <SectionTitle
          subtitle="Why Choose GreenScape AI"
          title="Traditional Review vs AI-Powered Review"
        />

        <div className="grid lg:grid-cols-2 gap-10">

          {/* Traditional */}

          <div className="bg-white rounded-3xl p-10 border border-red-100">

            <h3 className="text-2xl font-bold mb-8 text-red-600">

              Traditional Process

            </h3>

            <div className="space-y-6">

              {traditional.map((item, index) => (

                <div
                  key={index}
                  className="flex items-center gap-4"
                >

                  <XCircle
                    className="text-red-500"
                    size={24}
                  />

                  <span>{item}</span>

                </div>

              ))}

            </div>

          </div>

          {/* AI */}

          <div className="bg-green-600 rounded-3xl p-10 text-white shadow-xl">

            <h3 className="text-2xl font-bold mb-8">

              GreenScape AI

            </h3>

            <div className="space-y-6">

              {greenscape.map((item, index) => (

                <div
                  key={index}
                  className="flex items-center gap-4"
                >

                  <CheckCircle2
                    size={24}
                  />

                  <span>{item}</span>

                </div>

              ))}

            </div>

          </div>

        </div>

      </Container>

    </section>
  );
}