from __future__ import division
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def make_graphing_array(start_array):
	start_array=np.expand_dims(start_array,axis=1)
	end_array=np.concatenate((ballpark_array[:,[0,1]],start_array),axis=1)
	return end_array[end_array[:,2].argsort()]

def make_individual_graphing_array(items,new_array,hard=False):
	for item in items:
		row=int(item/5)
		col=item%5
		park=ballpark_array[row][1]
		if col==0:
			area="Left"
		elif col==1:
			area="Left Center"
		elif col==2:
			area="Center"
		elif col==3:
			area="Right Center"
		elif col==4:
			area="Right"
		energy=ballpark_array[row][col+2]
		launch_angle=ballpark_array[row][col+7]
		new_array=np.append(new_array,np.transpose(np.expand_dims(np.array([park,area,energy,launch_angle]),axis=1)),axis=0)
	if hard:
		return new_array[new_array[:,2].argsort()[::-1]]
	else:
		return new_array[new_array[:,2].argsort()]

# Open files
with open('ballparks.csv','rb') as filename:
	reader=csv.reader(filename)
	ballpark_array=np.empty((0,2))
	for row in filename:
		split_col=[x.strip() for x in row.split(',')]
		team_array=np.array([[split_col[0],split_col[1]]])
		ballpark_array=np.append(ballpark_array,team_array,axis=0)
	ballpark_array=np.delete(ballpark_array,(0),axis=0)
	# print ballpark_array

with open('ballparks_stats.csv','rb') as filename:
	reader=csv.reader(filename)
	stats_array=np.empty((0,10))
	for row in filename:
		split_col=[x.strip() for x in row.split(',')]
		park=np.array([split_col])
		stats_array=np.append(stats_array,park,axis=0)
	# print stats_array
ballpark_array=np.concatenate((ballpark_array,stats_array),axis=1)

# Get mean values for total parks and left/right handers
full_park=np.mean(ballpark_array[:,[2,3,4,5,6]].astype(np.float),axis=1)
left=np.mean(ballpark_array[:,[2,3]].astype(np.float),axis=1)
right=np.mean(ballpark_array[:,[5,6]].astype(np.float),axis=1)

average_home_run=np.mean(full_park)
average_left=np.mean(left)
average_right=np.mean(right)
# print average_home_run
# print average_left
# print average_right

# combine string and values
full_park=make_graphing_array(full_park)
left_park=make_graphing_array(left)
right_park=make_graphing_array(right)
full_park_percent_pos=[]
full_park_percent_neg=[]
left_percent_pos=[]
left_percent_neg=[]
right_percent_pos=[]
right_percent_neg=[]

# separate into percent differences from the average
for item in full_park[:,2].tolist():
	percent=100*(average_home_run-float(item))/average_home_run
	if percent<0:
		full_park_percent_neg.append(percent)
	else:
		full_park_percent_pos.append(percent)
for item in left_park[:,2].tolist():
	percent=100*(average_left-float(item))/average_left
	if percent<0:
		left_percent_neg.append(percent)
	else:
		left_percent_pos.append(percent)
for item in right_park[:,2].tolist():
	percent=100*(average_right-float(item))/average_right
	if percent<0:
		right_percent_neg.append(percent)
	else:
		right_percent_pos.append(percent)

# Get the top 10 easiest and hardest places
easy=np.argpartition(ballpark_array[:,[2,3,4,5,6]].astype(np.float),10,axis=None)[:10]
hard=np.argpartition(ballpark_array[:,[2,3,4,5,6]].astype(np.float),-10,axis=None)[-10:]
easy_array=np.empty((0,4))
hard_array=np.empty((0,4))
easy_array=make_individual_graphing_array(easy,easy_array)
hard_array=make_individual_graphing_array(hard,hard_array,hard=True)

# print easy_array
# print hard_array

# graph full park
ind=np.arange(float(len(full_park)))
ind_pos=np.arange(float(len(full_park_percent_pos)))
ind_neg=np.arange(float(len(full_park_percent_pos)),float(len(full_park_percent_pos))+float(len(full_park_percent_neg)))
alphas_pos=[float(i)/max(full_park_percent_pos) for i in full_park_percent_pos]
flip=[-x for x in full_park_percent_neg]
alphas_neg=[float(i)/max(flip) for i in flip]
rgba_colors_pos=np.zeros((len(full_park_percent_pos),4))
rgba_colors_pos[:,1]=1.0
rgba_colors_pos[:,3]=alphas_pos
rgba_colors_neg=np.zeros((len(full_park_percent_neg),4))
rgba_colors_neg[:,0]=1.0
rgba_colors_neg[:,3]=alphas_neg
fig = plt.figure(1)
ax= plt.subplot(111)
ax.bar(ind_pos,full_park_percent_pos,width=.7,color=rgba_colors_pos,linewidth=.1)
ax.bar(ind_neg,full_park_percent_neg,width=.7,color=rgba_colors_neg,linewidth=.1)
ax.plot((0,30),(0,0),'k')
ax.set_xticks(ind+.35)
ax.set_xticklabels(full_park[:,1].tolist(),rotation='60',ha='right')
ax.set_title('Ballparks Ranked by Average Minimum Energy to Hit a Home Run')
ax.set_ylabel('% Deviation from the average [x% easier]')
ax.grid(visible=True,axis='y')
ax.annotate('Average is 134.29 J', xytext=(1, -1), xy=(2,2))
plt.tight_layout()

# graph left handers
ind=np.arange(float(len(left_park)))
ind_pos=np.arange(float(len(left_percent_pos)))
ind_neg=np.arange(float(len(left_percent_pos)),float(len(left_percent_pos))+float(len(left_percent_neg)))
alphas_pos=[float(i)/max(left_percent_pos) for i in left_percent_pos]
flip=[-x for x in left_percent_neg]
alphas_neg=[float(i)/max(flip) for i in flip]
rgba_colors_pos=np.zeros((len(left_percent_pos),4))
rgba_colors_pos[:,1]=1.0
rgba_colors_pos[:,3]=alphas_pos
rgba_colors_neg=np.zeros((len(left_percent_neg),4))
rgba_colors_neg[:,0]=1.0
rgba_colors_neg[:,3]=alphas_neg
fig = plt.figure(2)
ax= plt.subplot(111)
ax.bar(ind_pos,left_percent_pos,width=.7,color=rgba_colors_pos,linewidth=.1)
ax.bar(ind_neg,left_percent_neg,width=.7,color=rgba_colors_neg,linewidth=.1)
ax.plot((0,30),(0,0),'k')
ax.set_xticks(ind+.35)
ax.set_xticklabels(left_park[:,1].tolist(),rotation='60',ha='right')
ax.set_title('Ballparks Ranked by Favorability to Left Handed Batters')
ax.set_ylabel('% Deviation from the average [x% easier]')
ax.grid(visible=True,axis='y')
ax.annotate('Average is 127.98 J', xytext=(1, -1), xy=(2,2))
plt.tight_layout()

# graph right handers
ind=np.arange(float(len(right_park)))
ind_pos=np.arange(float(len(right_percent_pos)))
ind_neg=np.arange(float(len(right_percent_pos)),float(len(right_percent_pos))+float(len(right_percent_neg)))
alphas_pos=[float(i)/max(right_percent_pos) for i in right_percent_pos]
flip=[-x for x in right_percent_neg]
alphas_neg=[float(i)/max(flip) for i in flip]
rgba_colors_pos=np.zeros((len(right_percent_pos),4))
rgba_colors_pos[:,1]=1.0
rgba_colors_pos[:,3]=alphas_pos
rgba_colors_neg=np.zeros((len(right_percent_neg),4))
rgba_colors_neg[:,0]=1.0
rgba_colors_neg[:,3]=alphas_neg
fig = plt.figure(3)
ax= plt.subplot(111)
ax.bar(ind_pos,right_percent_pos,width=.7,color=rgba_colors_pos,linewidth=.1)
ax.bar(ind_neg,right_percent_neg,width=.7,color=rgba_colors_neg,linewidth=.1)
ax.plot((0,30),(0,0),'k')
ax.set_xticks(ind+.35)
ax.set_xticklabels(right_park[:,1].tolist(),rotation='60',ha='right')
ax.set_title('Ballparks Ranked by Favorability to Right Handed Batters')
ax.set_ylabel('% Deviation from the average [x% easier]')
ax.grid(visible=True,axis='y')
ax.annotate('Average is 128.35 J', xytext=(1, -1), xy=(2,2))
plt.tight_layout()

# graph easy places
ind=np.arange(float(len(easy_array)))
rgba_colors=np.zeros((10,4))
rgba_colors[[0,4],:]=[.776,.047,.188,1]
rgba_colors[1]=[.984,.357,.122,1]
rgba_colors[[2,5],:]=[.110,.157,.255,1]
rgba_colors[[3,9],:]=[.475,.741,.933,1]
rgba_colors[6]=[.027,.157,.325,1]
rgba_colors[7]=[.988,.298,0.0,1]
rgba_colors[8]=[1.0,.78,.169,1]
rgba_colors[:,3]=.85
fig=plt.figure(4)
ax=plt.subplot(111)
bar_plot=ax.bar(ind,easy_array[:,2],color=rgba_colors,width=.7,linewidth=.1)
ax.set_xticks(ind+.35)
ax.set_xticklabels(easy_array[:,0].tolist(),rotation='60',ha='right')
ax.set_ylim(bottom=90,top=140)
ax.set_title('Easiest Places to Hit a Home Run with Optimal Launch Angle')
ax.set_ylabel('Energy in Joules [J]')
ax.grid(visible=True,axis='y')
average_line = mpatches.Patch(color='#FFFF00', label='Average Home Run Energy')
plt.legend(handles=[average_line])
ax.plot((0,10),(134.29,134.29),color='#FFFF00',linewidth=2)
i=0
for name in easy_array[:,1].tolist():
	height=bar_plot[i].get_height()
	ax.text(bar_plot[i].get_x()+bar_plot[i].get_width()/2.,1.03*height,name,ha='center',va='bottom',fontsize=10)
	i=i+1
i=0
for name in easy_array[:,3].tolist():
	height=bar_plot[i].get_height()
	ax.text(bar_plot[i].get_x()+bar_plot[i].get_width()/2.,1.01*height,name+u'\N{DEGREE SIGN}',ha='center',va='bottom',fontsize=10)
	i=i+1
plt.tight_layout()

#graph hard places
ind=np.arange(float(len(hard_array)))
rgba_colors=np.zeros((10,4))
rgba_colors[0]=[.027,.157,.325,1]
rgba_colors[1]=[.984,.357,.122,1]
rgba_colors[2]=[.047,.137,.251,1]
rgba_colors[3]=[.976,.259,.231,1]
rgba_colors[4]=[.0,.176,.384,1]
rgba_colors[5]=[.729,.071,.169,1]
rgba_colors[6]=[.729,.011,.180,1]
rgba_colors[7]=[.988,.298,.0,1]
rgba_colors[8]=[.110,.157,.255,1]
rgba_colors[9]=[.475,.741,.933,1]
rgba_colors[:,3]=.85
fig=plt.figure(5)
ax=plt.subplot(111)
bar_plot=ax.bar(ind,hard_array[:,2],color=rgba_colors,width=.7,linewidth=.1)
ax.set_xticks(ind+.35)
ax.set_xticklabels(hard_array[:,0].tolist(),rotation='60',ha='right')
ax.set_ylim(bottom=120,top=190)
ax.set_title('Hardest Places to Hit a Home Run with Optimal Launch Angle')
ax.set_ylabel('Energy in Joules [J]')
ax.grid(visible=True,axis='y')
plt.legend(handles=[average_line])
ax.plot((0,10),(134.29,134.29),color='#FFFF00',linewidth=2)
i=0
for name in hard_array[:,1].tolist():
	height=bar_plot[i].get_height()
	ax.text(bar_plot[i].get_x()+bar_plot[i].get_width()/2.,1.03*height,name,ha='center',va='bottom',fontsize=10)
	i=i+1
i=0
for name in hard_array[:,3].tolist():
	height=bar_plot[i].get_height()
	ax.text(bar_plot[i].get_x()+bar_plot[i].get_width()/2.,1.01*height,name+u'\N{DEGREE SIGN}',ha='center',va='bottom',fontsize=10)
	i=i+1
plt.tight_layout()


plt.show()