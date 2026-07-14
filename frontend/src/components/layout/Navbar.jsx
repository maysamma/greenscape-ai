import { Link } from "react-router-dom";
import { Leaf } from "lucide-react";

import Container from "../common/Container";
import Button from "../common/Button";

export default function Navbar() {

  return (

    <header className="sticky top-0 z-50 bg-white/90 backdrop-blur border-b border-slate-200">

      <Container>

        <div className="flex items-center justify-between h-20">

          {/* Logo */}

          <Link
            to="/"
            className="flex items-center gap-3"
          >

            <div className="bg-green-600 p-2 rounded-xl">

              <Leaf
                className="text-white"
                size={22}
              />

            </div>

            <div>

              <h1 className="font-bold text-xl">

                GreenScape AI

              </h1>

              <p className="text-xs text-slate-500">

                Design Smarter

              </p>

            </div>

          </Link>

          {/* Links */}

          <nav className="hidden md:flex gap-10 font-medium">

            <Link to="/">Home</Link>

            <Link to="/upload">Upload</Link>

            <Link to="/dashboard">Dashboard</Link>

            <Link to="/report">Report</Link>

          </nav>

          <Button>

            Get Started

          </Button>

        </div>

      </Container>

    </header>

  );

}