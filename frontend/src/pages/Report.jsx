import Container from "../components/common/Container";

import ReportHeader from "../components/report/ReportHeader";
import OverallScoreCard from "../components/report/OverallScoreCard";
import ExecutiveSummary from "../components/report/ExecutiveSummary";
import ScoreCard from "../components/report/ScoreCard";
import RecommendationCard from "../components/report/RecommendationCard";
import IssuesCard from "../components/report/IssuesCard";
import AgentSummary from "../components/report/AgentSummary";
import DownloadReport from "../components/report/DownloadReport";

export default function Report() {
  return (
    <section className="py-20 bg-slate-50 min-h-screen">

      <Container>

        <ReportHeader />

        <OverallScoreCard />

        <div className="mt-8">
          <ExecutiveSummary />
        </div>

        <div className="grid lg:grid-cols-2 gap-8 mt-8">

          <ScoreCard />

          <RecommendationCard />

        </div>

        <div className="grid lg:grid-cols-2 gap-8 mt-8">

          <IssuesCard />

          <AgentSummary />

        </div>

        <DownloadReport />

      </Container>

    </section>
  );
}