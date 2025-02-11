class Kam {
    public static void main(String[] args)
    {
        Vu v = new Vu("Homo");
        System.out.println(v.getLegning());
    }
}

class Vu {
    String legning;
    Vu(String legning) {
        this.legning = legning;
    }

    public String getLegning() {
        return legning;
    }
}