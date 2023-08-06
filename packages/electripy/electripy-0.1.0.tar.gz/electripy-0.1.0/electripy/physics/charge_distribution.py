from numpy import ndarray, array
from electripy.physics.charges import PointCharge


class _ChargesSet:
    """
    A _ChargesSet instance is a group of charges. The electric
    field at a given point can be calculated as the sum of each
    electric field at that point for every charge in the charge
    set.
    """

    def __init__(self, charges: list[PointCharge]) -> None:
        self.charges = charges

    def electric_field(self, point: ndarray) -> ndarray:
        """
        Returns the electric field at the specified point.
        """
        ef = array([0.0, 0.0])
        for charge in self.charges:
            ef += charge.electric_field(point)
        return ef

    def electric_force(self, charge: PointCharge) -> ndarray:
        """
        Returns the force of the electric field exerted
        on the charge.
        """
        ef = self.electric_field(charge.position)
        return ef * charge.charge

    def __getitem__(self, index):
        return self.charges[index]


class ChargeDistribution:
    def __init__(self):
        """
        There is one group for each charge in charges.
        Each group is a two dimensional vector. The first element is
        a charge, and the second element is the ChargeSet instance
        containing all charges in charges except the charge itself.
        """
        self.groups = []
        self.charges_set = _ChargesSet([])

    def add_charge(self, charge: PointCharge) -> None:
        """
        Adds the charge to charges_set and updates the groups.
        """
        self.charges_set.charges.append(charge)
        self._update_groups(self.charges_set.charges)

    def remove_charge(self, charge: PointCharge) -> None:
        """
        Removes the charge to charges_set and updates the groups.
        """
        self.charges_set.charges.remove(charge)
        self._update_groups(self.charges_set.charges)

    def _update_groups(self, charges: list[PointCharge]) -> None:
        """
        Let X be a charge from the charge distribution. Computing X electric
        force involves computing the electric force exerted on X by all
        the other charges on the charge distribution.

        This means that, in order to compute the electric force of X,
        we need a two dimensional vector where the first component is
        the charge X itself and the second component is a ChargeSet
        instance cointaning all charges on the charge distribution except
        X. This vector is called 'group'.
        """
        self.groups = []
        for charge in charges:
            self.groups.append(
                [
                    charge,
                    _ChargesSet([c for c in charges if c is not charge]),
                ]
            )

    def get_electric_forces(self) -> list[tuple[PointCharge, ndarray]]:
        """
        Returns a list of electric forces. There is one electric force for
        each charge in charges. Each electric force is a two dimensional
        vector. The first element is the charge and the second element is
        the electric force the other charges make on it.
        """
        electric_forces = []
        for group in self.groups:
            electric_forces.append((group[0], group[1].electric_force(group[0])))
        return electric_forces

    def get_electric_field(self, position: ndarray) -> ndarray:
        """
        Returns the electric force array at the given point.
        """
        return self.charges_set.electric_field(position)

    def __len__(self):
        return len(self.charges_set.charges)

    def __getitem__(self, index):
        return self.charges_set[index]
