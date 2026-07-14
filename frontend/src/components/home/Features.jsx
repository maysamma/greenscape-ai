import Container from "../common/Container";
import SectionTitle from "../common/SectionTitle";
import FeatureCard from "./FeatureCard";

import {
  Building2,
  Leaf,
  Lightbulb,
  Wind,
  Accessibility,
  ShieldCheck,
  DollarSign,
  Zap,
} from "lucide-react";

const features = [
  {
    icon: Building2,
    title: "Architecture Review",
    description:
      "Evaluate layout, circulation, room relationships and spatial efficiency.",
  },
  {
    icon: Leaf,
    title: "Sustainability",
    description:
      "Analyze sustainable design strategies and environmental impact.",
  },
  {
    icon: Zap,
    title: "Energy Efficiency",
    description:
      "Estimate energy performance and identify efficiency opportunities.",
  },
  {
    icon: Lightbulb,
    title: "Natural Lighting",
    description:
      "Assess daylight quality and optimize natural illumination.",
  },
  {
    icon: Wind,
    title: "Ventilation",
    description:
      "Review airflow and indoor environmental comfort.",
  },
  {
    icon: Accessibility,
    title: "Accessibility",
    description:
      "Ensure universal accessibility and inclusive architectural design.",
  },
  {
    icon: ShieldCheck,
    title: "Building Code",
    description:
      "Check compliance with building regulations and standards.",
  },
  {
    icon: DollarSign,
    title: "Cost Optimization",
    description:
      "Recommend design improvements while reducing construction costs.",
  },
];

export default function Features() {
  return (
    <section className="py-24 bg-slate-50">

      <Container>

        <SectionTitle
          subtitle="Powerful AI Features"
          title="Everything Architects Need"
        />

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">

          {features.map((feature, index) => (
            <FeatureCard
              key={index}
              {...feature}
            />
          ))}

        </div>

      </Container>

    </section>
  );
}