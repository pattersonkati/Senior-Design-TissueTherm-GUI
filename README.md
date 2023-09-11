# Senior-Design-TissueTherm-GUI
Last Updated: 9/11/2023

This repository is comprised of a user-friendly GUI that was created to support my Senior Design Project. 

The purpose of this senior design project was to create a testbed and user interface that will assist in the research of thermal effects of PEMF radiation on tissues. This system was most often tested with raw chicken breast. 

The user interface allows adjustments to be specific in its representation for each trial. The following is a guide to operating the GUI.

(1) Specify the shape of your sample (square/rectangle or circular/ellipsoid) <br/>
&nbsp (2) Specify the length and width of your sample <br/>
(3) Either upload a temperature file or collect data directly from the testbed <br/>
   (3a) For testing, an "arbitrary_temps.csv" was provided for upload <br/>
(4) Adjust the expected temperature rangeso the 3D thermal map can display in a visually maximizing way <br/>
(5) Select the thermal data representations to be generated (3D thermal map or Temperature Table) <br/>
(6) (Optional) Upload data of the electric and/or magnetic field sensors oscilloscope data to generate their graphs over time <br/>
   (6a) For testing, an "oscilloscope_eehh.csv" was provided for upload. The E-field sensors were on channel 1, and the H-field sensors were on channel 2 of the oscilloscope <br/>
   (6a) In this design, it was assumed that two of the electric field or two of the magnetic field sensors would be used, not just one. The data important here is the delta value of strenght between the two identical sensors, thus this is what is plotted.

