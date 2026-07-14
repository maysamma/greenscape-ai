import { ArrowRight } from "lucide-react";
import { Link } from "react-router-dom";

import Button from "../common/Button";
import Container from "../common/Container";

export default function CTA() {
  return (
    <section className="py-28">

      <Container>

        <div className="rounded-[40px] bg-gradient-to-r from-green-700 via-green-600 to-emerald-500 p-16 text-center text-white shadow-2xl">

          <h2 className="text-5xl font-bold">

            Ready to Analyze
            <br />
            Your Next Building?

          </h2>

          <p className="mt-8 max-w-3xl mx-auto text-lg text-green-100 leading-8">

            Upload your architectural floor plan and receive
            professional AI-powered sustainability analysis,
            building code review, energy evaluation,
            and intelligent recommendations.

          </p>

          <div className="mt-12">

            <Link to="/upload">

              <Button
                className="
                bg-white
                text-green-700
                hover:bg-slate-100
                inline-flex
                items-center
                gap-3
                "
              >

                Start Analysis

                <ArrowRight size={20}/>

              </Button>

            </Link>

          </div>

        </div>

      </Container>

    </section>
  );
}