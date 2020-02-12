#! python 
#%%
_settings = {
    "file"  : "r0102_rivtest.py",
    "path"  : "os.getcwd()",
    "title" : "my calc",  
    "html"  : "",
    "pdf"   : "",
    "opt"   : "(width), nodate, noclean, notoc",
    "tags"  : "concrete, beam, seismic, cracked, expoxy"
}
from rivet.rivet_lib import * 
ad_paths(_settings)
ad_flags()

#%%
i__(f""" [01] loads 
    
    The need to distinguish between the various meanings of "frame of
    reference" has led to a variety of ter ms. For example, sometimes the type
    of coordinate system is attached as a modifier, as in Cartesian frame of
    reference. Sometimes the state of motion asfda asd s fdas sfdfasdfasdf is
    emphasized, as in rotating frame of reference.
    
    Render image
    | file file.png | inserted png image | .5 
    | file file.jpg | inserted jpg image | .9 

    Render text
    | file file.txt | test text | 5  

    Render equation
    | file file.tex | ACI 318 2.2 | 1 

    Render inline equation
    | eq α = 3^2 * (2 + 5) / 7 | ACI 318 3.2 | 2  

""")
v__(f""" values abcd 
    
    Some text if needed

    a11 = 12.23  | description 1 
    a22 = 2.2    | description 2 
    a33 = 14     | description 3

""")
e__(f""" equations  abcd 
    
    Some introductory text.

    equation description1 | units | [2,2] 
    
    aa2 = a11*14

    equation description2 | units | [2,2]
    
    aa22 = aa2*5

""")
#%%
i__(f""" [02] analysis
    
    This is a test γ = 2*Σ of the system and this is a further test
    and another greek letter Γ₂.

    The need to distinguish between the various meanings of "frame of
    reference" has led to a variety of terms. For example, sometimes the type
    of coordinate

    | newpage

    The way it transforms to frames considered as related is emphasized as in
    Galilean frame of reference. Sometimes frames are distinguished by the
    scale of their observations, as in macroscopic and microscopic frames of
    reference.[1]
    
""")
v__(f""" stress
    
    this is one line 4 γ

    gg = 5.4    | height of roof 
    hh = 12.2   | height of balcony 

""")
e__(f""" some equations
    
    equation description3 | units | [2,2]

    xx1 = gg + 4
    
    equation description4 | units | [2,2]
    
    xx2 = hh + 10

""")
#%%
r__(f""" [03] a plot
    
    fig, ax1 = plt.subplots()
    t = arange(0.01, 10.0, 0.01)
    s1 = exp(t)
    ax1.plot(t, s1, 'b-')
    ax1.set_xlabel('time (s)')
    
    ax1.set_ylabel('exp', color='b')
    ax1.tick_params('y', colors='b')

    ax2 = ax1.twinx()
    s2 = sin(2 * pi * t)
    ax2.plot(t, s2, 'r.')
    ax2.set_ylabel('sin', color='r')
    ax2.tick_params('y', colors='r')

    fig.tight_layout()
    plt.savefig("testfig.png")
    
    #print(global_rivet_dict)

""")

