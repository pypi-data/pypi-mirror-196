import itertools
import numpy as np
from scipy.spatial.transform import Rotation

from pybendt.interaction import kB_in_kcal_per_mole_per_kelvin

class Reaction():
	id_iter = itertools.count()
	def __init__(self, atoms, reaction_conditions, effect_functions, effect_parameters, self_remove = True):
		self.id = next(Reaction.id_iter)+1
		self.atoms = atoms
		self.reaction_conditions = reaction_conditions
		self.effect_functions = effect_functions
		self.effect_parameters = effect_parameters
		self.self_remove = self_remove
	def conditions_fulfilled(self):
		return all([ rc.condition_fulfilled for rc in self.reaction_conditions ])
	def effect(self):
		for i in range(len(self.effect_functions)):
			self.effect_functions[i](**self.effect_parameters[i])
		if self.self_remove: remove_reaction_effect(self)
	def remove(self):
		for atom in self.atoms:
			atom.reactions = [ r for r in atom.reactions if r.id != self.id ]
		self.atoms = None
	def __str__(self):
		return '{}'.format(self.id)
		# atoms_string = ('{}-'*len(self.atoms)).format(*[a.id for a in self.atoms])[:-1]
		# return '#{} {} | conditions: {}, effects: {}'.format(self.id, atoms_string, self.condition_function.__name__, self.effect_function.__name__)
	def __repr__(self):
		return self.__str__()

class ReactionCondition():
	def __init__(self, atoms, condition_function, condition_parameters):
		self.atoms = atoms
		self.condition_function = condition_function
		self.condition_parameters = condition_parameters
		self.condition_fulfilled = False
	def evaluate_condition(self, condition_variable):
		self.condition_fulfilled = self.condition_function(condition_variable, **self.condition_parameters)
	def __str__(self):
		return '{} {}'.format(self.condition_function.__name__, self.condition_parameters)
	def __repr__(self):
		return self.__str__()

def distance_condition(distance, sign, reaction_distance):
	if sign == ">":
		return distance > reaction_distance
	elif sign == "<":
		return distance < reaction_distance
	elif sign == ">=":
		return distance >= reaction_distance
	elif sign == "<=":
		return distance <= reaction_distance
	else:
		1/0

def rmsd_condition(atoms, sign, reaction_rmsd, ref_atoms, dimension = 3):
	if sign == ">":
		return rmsd(atoms, ref_atoms, dimension) > reaction_rmsd
	elif sign == "<":
		return rmsd(atoms, ref_atoms, dimension) < reaction_rmsd
	elif sign == ">=":
		return rmsd(atoms, ref_atoms, dimension) >= reaction_rmsd
	elif sign == "<=":
		return rmsd(atoms, ref_atoms, dimension) <= reaction_rmsd
	else:
		1/0

# RETHINK PASSING TWO CONDITION VARIABLES
def metropolis_rmsd_condition(args, ref_atoms, exp_factor = 1, dimension = 3):
	atoms, random_number = args
	# print(atoms)
	# print(random_number)
	# print(ref_atoms)
	rmsd_value = rmsd(atoms, ref_atoms, dimension)
	# print(rmsd_value)
	# print(np.exp(-exp_factor*rmsd_value))
	# print()
	return random_number < np.exp(-exp_factor*rmsd_value)

# RETHINK PASSING THREE CONDITION VARIABLES
def metropolis_energy_condition(args, temperature):
	energy, ref_energy, random_number = args
	print(energy)
	print(ref_energy)
	print(random_number)
	print(np.exp((energy-ref_energy)/(kB_in_kcal_per_mole_per_kelvin*temperature)))
	print()
	# 1/0
	return random_number < np.exp((energy-ref_energy)/(kB_in_kcal_per_mole_per_kelvin*temperature))

def random_condition(random_number, probability):
	return random_number < probability

def rmsd(atoms, ref_atoms, dimension = 3):
	assert len(atoms)==len(ref_atoms), 'Reference structure for RMSD should have the same number of atoms as the simulated one'
	a = np.zeros((len(atoms), 3))
	b = np.zeros((len(ref_atoms), 3))
	for i in range(len(atoms)):
		if dimension == 3:
			a[i] = atoms[i].position
			b[i] = ref_atoms[i].position
		elif dimension == 2:
			a[i][0], a[i][1] = atoms[i].position
			b[i][0], b[i][1] = ref_atoms[i].position
		else:
			1/0
	a_gc = np.mean(a, axis = 0)
	b_gc = np.mean(b, axis = 0)
	_, rmsd = Rotation.align_vectors(a-a_gc, b-b_gc)
	return rmsd

def add_interaction_effect(atom1, atom2, interaction):
	print("interaction added")
	atom1.add_existing_interaction(atom2, interaction)

def remove_interaction_effect(interaction):
	print("interaction removed")
	interaction.remove()

def add_reaction_effect(atoms, reaction):
	print("reaction added")
	atoms[0].add_existing_reaction(atoms[1:], reaction)

def remove_reaction_effect(reaction):
	print("reaction removed")
	reaction.remove()

def end_simulation_effect():
	1/0