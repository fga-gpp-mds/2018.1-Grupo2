from django.shortcuts import render
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.http import HttpResponse
from pygithub_api_integration.models import Repository
from pygithub_api_integration.models import Contributor
from ranking_commiters.models import Weight

MARGIN_LEFT = 50
SPACE_VERT = 20
LINE = 213
CENTER_PAG = 300


def pdfView(request, repo_id):

    repo = Repository.objects.get(id=repo_id)
    commiters = Contributor.objects.filter(repository=repo_id)
    weight = Weight.objects.get(repository=repo_id)

    ranking_commiters = Contributor.getScore(commiters, weight)

    response = HttpResponse(content_type='application/pdf')
    report_name = 'attachment; filename=Relatorio_' + repo.full_name + '.pdf'
    response['Content-Disposition'] = report_name

    pdf = canvas.Canvas(response, pagesize=A4)

    pdf.setFont('Times-Bold', 26)
    pdf.drawString(MARGIN_LEFT, SPACE_VERT * 39.6, repo.full_name)

    pdf.line(MARGIN_LEFT, (LINE * 3.8) - 20,
             MARGIN_LEFT * 11, (LINE * 3.8) - 20)

    pdf.line(CENTER_PAG, 780, CENTER_PAG, 620)

    pdf.setFont('Times-Bold', 12)
    pdf.drawString(MARGIN_LEFT, SPACE_VERT * 38.65, "Ranking de Commiters:")

    line_down = 0

    for c in ranking_commiters:
        pdf.setFont('Times-Bold', 9)
        pdf.drawString(MARGIN_LEFT + 10, SPACE_VERT * (38 - line_down),
                       c.name + '/' + c.login + ' | ' + str(c.score))

        line_down += 0.65

    pdf.line(MARGIN_LEFT, (LINE * 3) - 28, MARGIN_LEFT * 11, (LINE * 3) - 28)

    pdf.drawImage('static/images/charts/chart_issue.png',
                  MARGIN_LEFT + 10, SPACE_VERT * 21,
                  width=300, height=190)

    pdf.line(MARGIN_LEFT, (LINE * 2) - 15, MARGIN_LEFT * 11, (LINE * 2) - 15)

    pdf.drawImage('static/images/charts/chart_commit.png',
                  MARGIN_LEFT + 10, SPACE_VERT * 11,
                  width=300, height=190)

    pdf.line(MARGIN_LEFT, LINE, MARGIN_LEFT * 11, LINE)

    pdf.drawImage('static/images/charts/chart_pr.png',
                  MARGIN_LEFT + 10, SPACE_VERT,
                  width=300, height=190)

    pdf.showPage()
    pdf.save()

    return response
