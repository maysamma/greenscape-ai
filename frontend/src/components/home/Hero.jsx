import { motion } from "framer-motion";
import Button from "../common/Button";
import Container from "../common/Container";

export default function Hero() {
  return (
    <section className="bg-gradient-to-b from-green-50 to-white py-24">
      <Container>

        <div className="grid lg:grid-cols-2 gap-12 items-center">

          {/* Left */}

          <motion.div
            initial={{ opacity: 0, x: -40 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: .8 }}
          >

            <span className="bg-green-100 text-green-700 px-4 py-2 rounded-full font-medium">
              AI-Powered Sustainable Design
            </span>

            <h1 className="text-6xl font-extrabold mt-8 leading-tight">

              Design Smarter.
              <br />
              Build Greener.

            </h1>

            <p className="text-slate-600 mt-8 text-lg leading-8">

              Upload your architectural floor plan and receive
              AI-powered sustainability analysis, building code review,
              energy evaluation, lighting assessment, and professional
              recommendations in minutes.

            </p>

            <div className="flex gap-5 mt-10">

              <Button className="bg-green-600 hover:bg-green-700 text-white">
                Start Analysis
              </Button>

              <Button className="bg-white border border-green-600 text-green-700 hover:bg-green-50">
                Watch Demo
              </Button>

            </div>

          </motion.div>

          {/* Right */}

          <motion.div
            initial={{ opacity:0,x:40 }}
            animate={{ opacity:1,x:0 }}
            transition={{ duration:.8 }}
            className="flex justify-center"
          >

            <img
              src="https://images.unsplash.com/photo-1511818966892-d7d671e672a2?w=800"
              alt="Architecture"
              className="rounded-3xl shadow-xl"
            />

          </motion.div>

        </div>

      </Container>
    </section>
  );
}