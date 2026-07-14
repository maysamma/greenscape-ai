from fastapi import APIRouter
from app.schemas.report import ReportResponse

router = APIRouter(
    prefix="/report",
    tags=["Report"]
)


@router.get("/{project_id}", response_model=ReportResponse)
async def get_report(project_id: str):

    return {

        "executive_summary":
            "The building demonstrates good sustainability and energy performance. Minor improvements are recommended for natural lighting and orientation.",

        "overall_score":92,

        "scores":{

            "energy":88,

            "lighting":94,

            "sustainability":91

        },

        "issues":[

            "Limited daylight in the north rooms.",

            "Insufficient natural ventilation in corridor."

        ],

        "recommendations":[

            "Increase window size.",

            "Improve building orientation.",

            "Add shading devices."

        ],

        "agents":[

            {

                "name":"Energy Agent",

                "score":88,

                "summary":"Energy efficiency is good."

            },

            {

                "name":"Lighting Agent",

                "score":94,

                "summary":"Natural lighting is excellent."

            },

            {

                "name":"Architecture Agent",

                "score":90,

                "summary":"Layout is functional."

            }

        ]

    }