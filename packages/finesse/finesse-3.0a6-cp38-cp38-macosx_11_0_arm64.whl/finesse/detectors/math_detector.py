from .general import Detector
from ..components.readout import ReadoutDetectorOutput
from finesse.detectors.workspace import DetectorWorkspace
from finesse.symbols import Symbol, Constant


class MathDetectorWorkspace(DetectorWorkspace):
    """MathDetectorWorkspace."""

    def __init__(self, owner, sim):
        self.expression = owner.expression
        if not isinstance(self.expression, Symbol):
            self.expression = Constant(self.expression)

        # Get all the detectors in the expression
        self.detectors = [  # will select constants, whose value is a detector
            a
            for a in self.expression.all(
                lambda a: isinstance(a.value, (Detector, ReadoutDetectorOutput))
            )
        ]
        out_wss = set(  # workspaces can be in both lists
            (*sim.readout_workspaces, *sim.detector_workspaces)
        )
        # find the workspaces for the detectors
        self.dws = []
        for det in self.detectors:
            for ws in out_wss:
                if ws.oinfo.name == det.value.name:
                    self.dws.append(ws)
        self.set_output_fn(self.__output)
        needs_carrier = any(_.needs_carrier for _ in self.dws)
        needs_signal = any(_.needs_signal for _ in self.dws)
        needs_noise = any(_.needs_noise for _ in self.dws)
        needs_modal_update = any(_.needs_modal_update for _ in self.dws)
        needs_simulation = (
            needs_carrier or needs_signal or needs_noise or needs_modal_update
        )
        super().__init__(
            owner,
            sim,
            needs_carrier=needs_carrier,
            needs_signal=needs_signal,
            needs_noise=needs_noise,
            needs_modal_update=needs_modal_update,
            needs_simulation=needs_simulation,
        )

    def __output(self, ws):
        subs = {a: ws.get_output() for a, ws in zip(self.detectors, self.dws)}
        return ws.expression.eval(subs=subs)


class MathDetector(Detector):
    """A detector that performs some math operation and outputs the result.

    Parameters
    ----------
    name : str
        Name of detector

    expression : Symbol
        Symbolic expression to evaluate as the detectors output

    Examples
    --------
    KatScript example:

        l l1 P=1
        pd P l1.p1.o
        fd E l1.p1.o f=l1.f
        bp qx l1.p1.o q x
        modes(maxtem=3)
        gauss g1 l1.p1.o w0=1m z=0

        mathd Y1 P*2
        mathd Y2 P**2
        mathd Y3 cos(1+P**2)
        mathd Y4 E*2
        mathd Y5 qx+1
    """

    def __init__(self, name, expression):
        super().__init__(name, dtype="O")
        self.expression = expression

    @property
    def needs_fields(self):
        return False

    @property
    def needs_trace(self):
        return False

    def _get_workspace(self, sim):
        return MathDetectorWorkspace(self, sim)
