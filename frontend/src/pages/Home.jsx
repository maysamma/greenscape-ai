import { Link } from "react-router-dom";
import Layout from "../components/layout/Layout";
import FeatureCard from "../components/home/FeatureCard";

export default function Home() {
  return (
    <Layout>
      {/* Hero Section */}
      <section className="flex flex-col items-center justify-center py-20">

        <h1 className="text-6xl font-bold text-green-700">
          GreenScape AI
        </h1>

        <p className="mt-6 max-w-3xl text-center text-gray-600 text-xl">
          AI-powered platform for reviewing architectural designs,
          improving sustainability, energy efficiency,
          accessibility, and building code compliance.
        </p>

        <Link
          to="/upload"
          className="mt-10 rounded-xl bg-green-700 px-8 py-4 text-lg font-semibold text-white transition hover:bg-green-800"
        >
          Start New Analysis
        </Link>

      </section>

      {/* Features */}
      <section className="mt-20">

        <h2 className="text-center text-4xl font-bold">
          Features
        </h2>

        <div className="mt-10 grid gap-6 md:grid-cols-2 xl:grid-cols-3">

          <FeatureCard
            icon="🌱"
            title="Sustainability"
            description="Evaluate sustainable architectural practices."
          />

          <FeatureCard
            icon="⚡"
            title="Energy Analysis"
            description="Analyze energy efficiency."
          />

          <FeatureCard
            icon="♿"
            title="Accessibility"
            description="Verify accessibility standards."
          />

          <FeatureCard
            icon="🏢"
            title="Building Code"
            description="Review compliance with regulations."
          />

          <FeatureCard
            icon="💡"
            title="Lighting"
            description="Evaluate natural lighting."
          />

          <FeatureCard
            icon="📄"
            title="AI Report"
            description="Generate a professional AI report."
          />

        </div>

      </section>

      {/* Footer */}
      <footer className="mt-24 border-t py-8 text-center text-gray-500">
        GreenScape AI © 2026
      </footer>

    </Layout>
  );
}