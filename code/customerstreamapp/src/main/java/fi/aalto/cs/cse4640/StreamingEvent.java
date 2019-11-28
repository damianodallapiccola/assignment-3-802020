package fi.aalto.cs.cse4640;


import java.util.Date;


public class StreamingEvent {
    public Integer part_id;
    public String ts_date;
    public String ts_time;
    public String room;

    StreamingEvent() {

    }
    StreamingEvent(int part_id, String ts_date, String ts_time, String room) {
        this.part_id = part_id;
        this.ts_date = ts_date;
        this.ts_time = ts_time;
        this.room = room;
    }
    public String toString() {
        return "part_id="+ part_id.toString() + " ts_date=" + ts_date + " ts_time=" + ts_time + " room="+room;
    }
}
