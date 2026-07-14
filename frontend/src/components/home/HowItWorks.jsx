import {
  Upload,
  ScanSearch,
  BrainCircuit,
  FileText,
} from "lucide-react";

import Container from "../common/Container";
import SectionTitle from "../common/SectionTitle";

const steps = [
  {
    icon: Upload,
    title: "Upload Floor Plan",
    description:
      "Upload your architectural floor plan in PDF, PNG or JPG format.",
  },
  {
    icon: ScanSearch,
    title: "Vision Analysis",
    description:
      "Computer Vision extracts rooms, walls, dimensions and building information.",
  },
  {
    icon: BrainCircuit,
    title: "Multi-Agent Review",
    description:
      "Specialized AI agents evaluate sustainability, energy, lighting, ventilation and compliance.",
  },
  {
    icon: FileText,
    title: "Professional Report",
    description:
      "Receive a complete report with scores, recommendations and improvement priorities.",
  },
];

export default function HowItWorks() {
  return (
    <section className="py-24 bg-white">
      <Container>

        <SectionTitle
          subtitle="Simple Process"
          title="How GreenScape AI Works"
        />

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-10">

          {steps.map((step, index) => {

            const Icon = step.icon;

            return (

              <div
                key={index}
                className="relative text-center"
              >

                <div className="mx-auto w-20 h-20 rounded-full bg-green-100 flex items-center justify-center">

                  <Icon
                    size={34}
                    className="text-green-600"
                  />

                </div>

                <div className="absolute -top-3 -right-3 bg-green-600 text-white w-8 h-8 rounded-full flex items-center justify-center font-bold">

                  {index + 1}

                </div>

                <h3 className="mt-8 text-xl font-bold">

                  {step.title}

                </h3>

                <p className="mt-4 text-slate-500 leading-7">

                  {step.description}

                </p>

              </div>

            );

          })}

        </div>

      </Container>
    </section>
  );
}