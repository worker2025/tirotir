from pathlib import Path
root=Path(__file__).parent.parent/'examples'
names=['official_program','hello_world','sum_two_numbers','simple_calculator','even_or_odd','age_checker','average','maximum','minimum','counting','multiplication_table','sum_list','factorial','fibonacci','search_list','simple_sort','grade_average','guessing_game','names_list','person_dictionary','related_functions','nested_loops','break_demo','continue_demo','recursion','text_processing','character_count','unit_conversion','area_calculation','simple_menu','combined_project','creative_square','triangle','rectangle','circle','colored_motion','spiral','star','geometric_pattern','pen_up_down','clear_scene','short_note','high_note','low_note','simple_melody','moving_ball','rotating_shape','flower','house','creative_project','gui_basics']
files=sorted(root.glob('*.tirotir'))
if len(files)>len(names): raise SystemExit(f'too many files: {len(files)}')
tmp=[]
for i,f in enumerate(files):
 target=root/f'{i:02d}_{names[i]}.tirotir'
 if f.name==target.name: continue
 t=f.with_suffix('.tmp.tirotir'); f.rename(t); tmp.append((t,target))
for t,target in tmp:
 target.parent.mkdir(exist_ok=True); t.rename(target)
print(f'renamed {len(files)} examples')
