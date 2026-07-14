import Container from "../common/Container";

export default function Footer() {

  return (

    <footer className="bg-slate-900 text-white py-12 mt-20">

      <Container>

        <div className="flex flex-col md:flex-row justify-between gap-10">

          <div>

            <h2 className="text-2xl font-bold">

              GreenScape AI

            </h2>

            <p className="text-slate-400 mt-3 max-w-sm">

              AI-powered architectural design review platform
              for sustainable and intelligent buildings.

            </p>

          </div>

          <div>

            <h3 className="font-semibold mb-3">

              Quick Links

            </h3>

            <ul className="space-y-2 text-slate-400">

              <li>Home</li>

              <li>Upload</li>

              <li>Dashboard</li>

              <li>Report</li>

            </ul>

          </div>

        </div>

        <div className="border-t border-slate-700 mt-10 pt-6 text-center text-slate-500">

          © 2026 GreenScape AI. All rights reserved.

        </div>

      </Container>

    </footer>

  );

}