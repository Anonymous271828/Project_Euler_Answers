def fibonacci(numbers):
    print(numbers[::-1][1], numbers[::-1][0])
    print("")
    if len(list(str(numbers[::-1][0]))) >= 1000:
        return len(numbers)
    numbers.append(numbers[::-1][0] + numbers[::-1][1])
    return fibonacci(numbers)
print(len(str(6907143411288613662029316540438748220025020428523316151407502968085995496570731490178932065075353329573175983583365088131600576901069947313063661206137698059523035486750311009034363281801031149232038101130690459628599068442120896374351565048450960211044867264278744540088190066612691510216877931796510239592974159758521233450749350495299337636637285776241643634185027355728459778865393627274053633368226072089077036319794467988295427029972166561022522254178441369531136476547100655478407088892226010575278068588496010463063007177360529111566365507388182034164205449907544161130907989998652504854205650027290305134362126360905154489110405770568395304647614639528230296602005360608134471946723714281162409152406026973534790176316804888707561071132227528074204891839601632219270643934385670580955490488128028298037145981568964933173791)))
#fibonacci([4268849393346257380470849705644932775877693719490817733589050470958012634473353356467113701758544957952213823210321472444139944273246821073700883689076601619476426701504572169382952887269412289457553084888914020119257641062748779076459623629537454182285440509719343432250671985000681901145856879405915572799468970357042636387377246110279664517417549469953106992374900834988785201608454482675955244895894338424653382255873661606073291106477894453161081450187160200067785170479459617676996020393210508449691830416857855909894964025282314885117553093195783331073870162078183802386311928680263599080208505050738706172797954622338925938145840885557978360096655962883066332450015483826163377773191520843267931679831517880335280359481351989671709682394323657499145101121176852714963621498812411179012739577193955729690515215968724306546306, 6907143411288613662029316540438748220025020428523316151407502968085995496570731490178932065075353329573175983583365088131600576901069947313063661206137698059523035486750311009034363281801031149232038101130690459628599068442120896374351565048450960211044867264278744540088190066612691510216877931796510239592974159758521233450749350495299337636637285776241643634185027355728459778865393627274053633368226072089077036319794467988295427029972166561022522254178441369531136476547100655478407088892226010575278068588496010463063007177360529111566365507388182034164205449907544161130907989998652504854205650027290305134362126360905154489110405770568395304647614639528230296602005360608134471946723714281162409152406026973534790176316804888707561071132227528074204891839601632219270643934385670580955490488128028298037145981568964933173791])
numbers = [1, 1]
while True:
    #print(numbers[::-1][1], numbers[::-1][0])
    #print("")
    if len(list(str(numbers[::-1][0]))) >= 1000:
        print(len(numbers), len(str(numbers[::-1][0])))
        break
    numbers.append(numbers[::-1][0] + numbers[::-1][1])