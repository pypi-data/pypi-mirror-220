import holoviews as hv
import panel as pn
from mortgage import Loan
import param

hv.extension("bokeh")


class MortgageSimulator(param.Parameterized):
    principal = param.Number(default=200000, bounds=(0, 1000000))
    interest = param.Number(default=0.06, bounds=(0.0001, 0.2), step=0.001)
    term = param.Integer(default=24, bounds=(0, 100))

    @param.depends("principal", "interest", "term")
    def update(self):
        loan = Loan(
            principal=self.principal, interest=self.interest, term=self.term
        )
        balance = []
        principal = []
        month = []

        month_dim = hv.Dimension("month", label="mortgage month", unit="m")
        balance_dim = hv.Dimension("balance", unit="£")
        principal_dim = hv.Dimension("principal", unit="£")

        for i in range(1, self.term):
            balance.append(float(loan.schedule(i).balance))
            principal.append(float(loan.schedule(i).principal))
            month.append(i)

        main = hv.Overlay()
        main += hv.Curve((month, balance), month_dim, balance_dim)
        main += hv.Curve((month, principal), month_dim, principal_dim)
        return main


mort_sim = MortgageSimulator()
dmap = hv.DynamicMap(mort_sim.update)

main = pn.Row(mort_sim.param, dmap)
main.show()
