/**********************************************************************
 UDF to write all cell volumes to a file
 ***********************************************************************/
 #include "udf.h"
 DEFINE_ON_DEMAND(on_demand_calc)
 {
	 Domain *d; /* declare domain pointer since it is not passed as an
	 argument to the DEFINE macro */
	 FILE *fp;
	 real volume,vol_tot;
	 Thread *t;
	 cell_t c;
	 d = Get_Domain(1); /* Get the domain using Ansys Fluent utility */
	 fp = fopen("H:\\volumedata.csv","a");
	 printf("File created\n");
	 thread_loop_c(t,d) /* Loop over all cell threads in the domain */	 
	 {	 
		begin_c_loop(c,t) /* Loop over all cells */
		 {
			 volume = C_VOLUME(c,t); /* get cell volume */
			 fprintf(fp,"%.20f\n",volume);
			 vol_tot += volume;
		 }
		 end_c_loop(c,t)
	 }
	 fclose(fp);
	 printf("File closed\n");
 } 