import random
import pandas as pd
import json

def create_sameple(n: int) -> list:
  """random subject
  Args:
      n (int): amount of random subject
  Returns:
      list: random subject
  """
  subj = ["Algorithms", "Machine Learning", "Data Structures", "Deep Learning", "Databases", "Artificial Intelligence", "Computer Vision", "Natural Language Processing", "Reinforcement Learning", "Big Data"]
  grade = ["A", "B+", "B", "C+", "C", "D+", "D", "F"]
  weight = ['1','2','3','4','5','6','7']
  selected_subj = random.sample(subj, n)
  fakes = [[subject, random.choice(grade), random.choice(weight)] for subject in selected_subj]
  fakes_str = [",".join(i) for i in fakes]
  fakes_str = "|".join(fakes_str)
  return fakes_str

class PoorGrader:
  grade = [["A", 4],
           ["B+", 3.5],
           ["B", 3],
           ["C+", 2.5],
           ["C", 2],
           ["D+", 1.5],
           ["D", 1],
           ["F", 0]] 
  
  def __init__(self) -> None:
    self.data = []
    self.Average_grade = None
    
  def start(self):
    """Start process of PoorGrader
    """
    self.read_json()
    while True:
      print("""Please select service code
1 Add Subject
2 Remove Subject
3 Calculate Grade
4 Show Subject 
5 Exit """)
      serviceCode = input("Enter service 1-5 : ")
      print("")
      #Let user choose service
      match serviceCode:
        case "1" :
          self.add_data()
          if self.continue_process():
              continue
          break
        case "2" :
          self.remove_data()
          if self.continue_process():
              continue
          break
        case "3" :
          print(f"Average Grade : {self.calculate_grade():.2f}")
          if self.continue_process():
              continue
          break
        case "4" :
          self.show_data()
        case "5" :
          # print("Exit Success")
          self.write_json()
          break
        case _ :
          print("Incorrect Service Code. Pleas try again\n")
          continue
  
  def add_data(self) -> None:
    """Add Subject to instance
    """
    print("""please enter subjects you want to add
Example : Math,A,3|English,B+,3|GE,B,3...
          """)
    try:
      data = input("input : ")
      data = data.split("|")
      data = [i.split(",") for i in data]
      for datum in data:
        if datum[0].lower() not in [i[0].lower() for i in self.data]: #check if input have already in instance?
          if datum[1] not in [i[0] for i in PoorGrader.grade]:
            print(f"{datum[0]} grade error please assign again in next process\n")
            continue
          self.data.append([datum[0], datum[1], int(datum[2])])
        else: # ask for overwrite data?
          while True:
            ask = input("The subject have already registed.\nDo you want to overwrite?\nY/y : yes | N,n : No\n: ")
            match ask:
              case _ if ask in ["Y",'y']:
                overwrite = [i for i in self.data if datum[0].lower()==i[0].lower()]
                self.data.remove(overwrite[0])
                if datum[1] not in [i[0] for i in PoorGrader.grade]:
                  print(f"{datum[0]} grade error please assign again in next process\n")
                  continue
                self.data.append([datum[0], datum[1], int(datum[2])])
                break
              case _ if ask in ["N",'n']:
                break
              case _ :
                continue
    except Exception as e:
      print('Wrong Format input. Please try again\n')
      self.add_data()
    self.calculate_grade()
    
  def remove_data(self) -> None:
      """remove subject form instance
      """
      print("""please enter subjects you want to remove
Example : Math|English|GE...
          """)
      try:
        removeSubj = input("input : ")
        removeSubj = removeSubj.split("|")
        removeSubj = [i.lower() for i in removeSubj]
        for i in self.data :
            if i[0].lower() in removeSubj:
                self.data.remove(i)
                removeSubj.remove(i[0].lower())
        if removeSubj: #Check no data to remove
          _str = "|".join(removeSubj)
          print(f"No {_str} in instance\n")
        self.calculate_grade()
      except Exception as e:
        print('Wrong Format input. Please try again\n')
        self.remove_data()

  def show_data(self) -> None:
    """show subject and average grade in pandas dataframe
    """
    show = pd.DataFrame(columns=["Subject", "Grade", "Weight"],
                        data=self.data
                        )
    print(show)
    print(f"Average Grade : {self.calculate_grade():.2f}\n")
  
  def calculate_grade(self) -> float:
    """Calculate Average grade of all subject
    Returns:
        float: Grade in decimal form
    """
    sum_score = self.tree_sum([self.map_grade(i[1])*(i[2]) for i in self.data])
    sum_weight = self.tree_sum([(i[2]) for i in self.data])
    self.Average_grade = sum_score/sum_weight
    return self.Average_grade
  
  def read_json(self):
    with open("Grade.json", 'r') as file:
      data = json.load(file)
    if data:
      self.data = [list(i.values()) for i in data]
    
  def write_json(self):
    pre_dict = [{"Subject" : i[0], "Grade" : i[1], "Weight" : i[2]} for i in self.data]
    with open("Grade.json", 'w') as file:
      json.dump(pre_dict, file, indent=4)
    
  @staticmethod
  def continue_process() -> bool:
    """Check continue process in loop
    Returns:
        bool: if continue return "True" if cancel process return "False"
    """
    continue_ = input("Continue?\nY/y : yes | N,n : No\n: ")
    match continue_:
      case _ if continue_ in ["Y", 'y']:
        return True
      case _ if continue_ in ["N", 'n']:
        print("Cancel Success")
        return False
      case _:
        return PoorGrader.continue_process()
  
  @staticmethod
  def map_grade(grade:str):
    """Map grade letter to numerical grade
    Args:
        grade (str): grade in letter form
    Returns:
        int: numerical grade form
    """
    return [i[1] for i in PoorGrader.grade if i[0] == grade][0]
  
  @staticmethod
  def tree_sum(data:list) -> float:
    """Calculate summation value
    Args:
        data (list): list to find summation value
    Returns:
        float: summation value
    """
    summation=0
    for i in data:
      summation+=i
    return summation
    
def main() -> None:
  print(create_sameple(5))
  test = PoorGrader()
  test.start()
  
if __name__ == "__main__":
  main()
  