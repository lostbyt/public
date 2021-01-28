
class Patient:

    """
    Patient informations and updates managment.
    """

    def __init__(self, name, age, sex, bmi, num_of_children, smoker):
        self.name = name
        self.age = age
        self.sex = sex
        self.bmi = bmi
        self.num_of_children = num_of_children
        self.smoker = smoker

    def estimated_insurance_cost(self):
        try:
            estimated_cost = 250 * self.age - 128 * self.sex + 370 * self.bmi + 425 * self.num_of_children + 24000 * self.smoker - 12500
            return "{patient_name}'s estimated insurance costs is {estimated_cost} dollars.".format(patient_name = self.name, estimated_cost= estimated_cost)
        except:
            return "Wrong input datas"

    def update_age(self, new_age):
        self.age = new_age
        recall_cost = self.estimated_insurance_cost()
        try:
            return "{patient_name} is now {patient_age} years old. {r}".format(patient_name= self.name, patient_age = self.age, r = recall_cost )
        except:
            return "Wrong input datas"


    def update_num_of_children(self, new_num_of_children):
        self.num_of_children = new_num_of_children
        recall_cost = self.estimated_insurance_cost()

        try:
            if self.num_of_children == 1:
                return "{patient_name} has {patient_s_number_of_children} child. {recall}".format(patient_name = self.name, patient_s_number_of_children = self.num_of_children, recall = recall_cost)
            else:
                return "{patient_name} has {patient_s_number_of_children} children. {recall}".format(patient_name = self.name, patient_s_number_of_children = self.num_of_children, recall = recall_cost)
        except:
            "Wrong input datas"

    def patient_profile(self):
        patient_information = {}
        patient_information["name"] = self.name
        patient_information["age"] = self.age
        patient_information["sex"] = self.sex
        patient_information["bmi"] = self.bmi
        patient_information["num_of_children"] = self.num_of_children
        patient_information["smoker"] = self.smoker
        return patient_information



datas_patient1 = ["Bob_fox", 27, 1, 23.7, 0, 1]
patient1 = Patient(*datas_patient1)
print(patient1.patient_profile())

