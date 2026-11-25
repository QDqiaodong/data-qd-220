from fractions import Fraction


def num(value,name):
    if not isinstance(value,str) or not value or len(value)>32: raise ValueError(f"{name} must be decimal string")
    try: return Fraction(value)
    except (ValueError,ZeroDivisionError) as exc: raise ValueError(f"invalid {name}") from exc


def txt(value): return str(value.numerator) if value.denominator==1 else f"{value.numerator}/{value.denominator}"


def process(data):
    peaks=data.get("peaks") if isinstance(data,dict) else None
    max_charge=data.get("max_charge") if isinstance(data,dict) else None
    tolerance=num(data.get("tolerance_mz"),"tolerance_mz")
    if not isinstance(peaks,list) or not 1<=len(peaks)<=10000: raise ValueError("peaks must contain 1..10000 items")
    if isinstance(max_charge,bool) or not isinstance(max_charge,int) or not 1<=max_charge<=20: raise ValueError("max_charge must be 1..20")
    if tolerance<0: raise ValueError("tolerance must be nonnegative")
    ids=set(); parsed=[]; previous=None
    for row in peaks:
        pid=row.get("id") if isinstance(row,dict) else None
        mz=num(row.get("mz"),"mz"); intensity=num(row.get("intensity"),"intensity")
        if not isinstance(pid,str) or not pid or pid in ids: raise ValueError("peak ids must be unique")
        if mz<=0 or intensity<0 or (previous is not None and mz<=previous): raise ValueError("peaks must increase in mz")
        previous=mz; ids.add(pid); parsed.append((pid,mz,intensity))
    assigned=set(); clusters=[]
    for index,(pid,mz,intensity) in enumerate(parsed):
        if pid in assigned: continue
        candidates=[]
        for charge in range(1,max_charge+1):
            spacing=Fraction(1,charge); members=[parsed[index]]; next_number=1
            for candidate in parsed[index+1:]:
                target=mz+spacing*next_number
                error=abs(candidate[1]-target)
                if error<=tolerance:
                    members.append(candidate); next_number+=1
                elif candidate[1]>target+tolerance:
                    break
            if len(members)>=2:
                max_error=max(abs(member[1]-(mz+spacing*n)) for n,member in enumerate(members))
                candidates.append((len(members),-max_error,-charge,charge,members,max_error))
        if not candidates: continue
        _,_,_,charge,members,max_error=max(candidates)
        if any(member[0] in assigned for member in members): continue
        for member in members: assigned.add(member[0])
        clusters.append({"cluster_id":f"c{len(clusters)+1}","monoisotopic_peak_id":pid,"charge":charge,"peak_ids":[x[0] for x in members],"total_intensity":txt(sum((x[2] for x in members),Fraction(0))),"max_spacing_error_mz":txt(max_error)})
    unassigned=[pid for pid,_,_ in parsed if pid not in assigned]
    return {"clusters":clusters,"unassigned_peak_ids":unassigned}
