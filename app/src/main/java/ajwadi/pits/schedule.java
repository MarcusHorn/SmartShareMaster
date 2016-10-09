package ajwadi.pits;

import android.app.DatePickerDialog;
import android.app.Dialog;
import android.content.Context;
import android.graphics.Color;
import android.net.Uri;
import android.os.Bundle;
import android.os.Handler;
import android.support.v4.app.DialogFragment;
import android.support.v4.app.Fragment;
import android.text.InputType;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.DatePicker;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;

public class schedule extends Fragment {


    EditText from;
    EditText to;

    public class SelectDateFragmentTo extends DialogFragment implements DatePickerDialog.OnDateSetListener {

        @Override
        public Dialog onCreateDialog(Bundle savedInstanceState) {
            final Calendar calendar = Calendar.getInstance();
            int dayOfYear = calendar.get(Calendar.DAY_OF_YEAR);
            int yy = calendar.get(Calendar.YEAR);
            int mm = calendar.get(Calendar.MONTH);
            int dd = calendar.get(Calendar.DAY_OF_MONTH);

            DatePickerDialog dpd = new DatePickerDialog(getActivity(),this,yy,mm,dd);
            calendar.add(Calendar.DATE, 366-dayOfYear);
            dpd.getDatePicker().setMaxDate(calendar.getTimeInMillis());

            calendar.add(Calendar.DATE, -365);
            dpd.getDatePicker().setMinDate(calendar.getTimeInMillis());

            return dpd;
        }

        public void onDateSet(DatePicker view, int yy, int mm, int dd) {
            populateSetDate(yy, mm+1, dd);
        }

        public void populateSetDate(int year, int month, int day) {
            //Toast.makeText(getActivity(), month+"/"+day+"/"+year, Toast.LENGTH_SHORT).show();
            final Toast toast = Toast.makeText(getActivity(), "Pick a To Date", Toast.LENGTH_SHORT);
            //toast.show();

            Handler handler = new Handler();
            handler.postDelayed(new Runnable() {
                @Override
                public void run() {
                    toast.cancel();
                }
            }, 300);
            //The following code makes sure a 0 is placed in accordance to the policy

            to = (EditText) getActivity().findViewById(R.id.to);

            String Newdate;
            String monthS = new String();
            String dayS = new String();
            if (month<10){
                monthS = "0"+month;
            }else if (month >= 10){
                monthS = ""+month;
            }

            if (day<10){
                dayS = "0"+day;
            }else if (day >=10){
                dayS = ""+day;
            }
            //Toast.makeText(getActivity(), "Homie you picked: "+monthS+"."+dayS+"."+year, Toast.LENGTH_SHORT).show();
            to.setText(year+"-"+monthS+"-"+dayS);
            // dob.setText(month+"/"+day+"/"+year);
        }

    }

    public class SelectDateFragmentFrom extends DialogFragment implements DatePickerDialog.OnDateSetListener {

        @Override
        public Dialog onCreateDialog(Bundle savedInstanceState) {
            final Calendar calendar = Calendar.getInstance();
            int dayOfYear = calendar.get(Calendar.DAY_OF_YEAR);
            int yy = calendar.get(Calendar.YEAR);
            int mm = calendar.get(Calendar.MONTH);
            int dd = calendar.get(Calendar.DAY_OF_MONTH);

            DatePickerDialog dpd = new DatePickerDialog(getActivity(),this,yy,mm,dd);
            calendar.add(Calendar.DATE, 366-dayOfYear);
            dpd.getDatePicker().setMaxDate(calendar.getTimeInMillis());

            calendar.add(Calendar.DATE, -365);
            dpd.getDatePicker().setMinDate(calendar.getTimeInMillis());

            return dpd;
        }

        public void onDateSet(DatePicker view, int yy, int mm, int dd) {
            populateSetDate(yy, mm+1, dd);
        }

        public void populateSetDate(int year, int month, int day) {
            //Toast.makeText(getActivity(), month+"/"+day+"/"+year, Toast.LENGTH_SHORT).show();
            final Toast toast = Toast.makeText(getActivity(), "Pick a From Date", Toast.LENGTH_SHORT);
            //toast.show();

            Handler handler = new Handler();
            handler.postDelayed(new Runnable() {
                @Override
                public void run() {
                    toast.cancel();
                }
            }, 300);
            //The following code makes sure a 0 is placed in accordance to the policy

            from = (EditText) getActivity().findViewById(R.id.from);

            String Newdate;
            String monthS = new String();
            String dayS = new String();
            if (month<10){
                monthS = "0"+month;
            }else if (month >= 10){
                monthS = ""+month;
            }

            if (day<10){
                dayS = "0"+day;
            }else if (day >=10){
                dayS = ""+day;
            }
            //Toast.makeText(getActivity(), "Homie you picked: "+monthS+"."+dayS+"."+year, Toast.LENGTH_SHORT).show();
            from.setText(year+"-"+monthS+"-"+dayS);
            // dob.setText(month+"/"+day+"/"+year);
        }

    }




    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View rootView = inflater.inflate(R.layout.fragment_schedule, container, false);

        final EditText jhumma1 = (EditText) rootView.findViewById(R.id.from);
        final EditText jhumma2 = (EditText) rootView.findViewById(R.id.to);

        EditText from_date = (EditText) rootView.findViewById(R.id.from);
        EditText to_date = (EditText) rootView.findViewById(R.id.to);
        to_date.setInputType(InputType.TYPE_NULL);
        from_date.setInputType(InputType.TYPE_NULL);

        to_date.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View arg0) {

                DialogFragment newFragment = new SelectDateFragmentTo();
                newFragment.show(getFragmentManager(), "DatePicker");

            }
        });

        from_date.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View arg0) {

                DialogFragment newFragment = new SelectDateFragmentFrom();
                newFragment.show(getFragmentManager(), "DatePicker");

            }
        });

        return rootView;
    }



}
