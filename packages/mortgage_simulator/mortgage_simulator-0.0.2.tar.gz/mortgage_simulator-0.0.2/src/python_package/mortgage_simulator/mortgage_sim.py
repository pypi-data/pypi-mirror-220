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
        for i in range(1, self.term):
            balance.append(float(loan.schedule(i).balance))
            principal.append(float(loan.schedule(i).principal))
        return (
            hv.Curve(balance, label="balance")
            + hv.Curve(principal, label="principal")
        ).opts(shared_axes=False)


mort_sim = MortgageSimulator()
dmap = hv.DynamicMap(mort_sim.update)


main = pn.Row(mort_sim.param, dmap)
main.show()
