import Hero from "../components/home/Hero";
import Statistics from "../components/home/Statistics";
import Features from "../components/home/Features";
import HowItWorks from "../components/home/HowItWorks";
import WhyGreenScape from "../components/home/WhyGreenScape";
import CTA from "../components/home/CTA";

export default function Home() {
  return (
    <>
      <Hero />
      <Statistics />
      <Features />
      <HowItWorks />
      <WhyGreenScape />
      <CTA />
    </>
  );
}