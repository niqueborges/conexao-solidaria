from core.exceptions import AudioStreamNotFoundException, InstitutionNotFoundException

def test_exceptions():
    e1 = AudioStreamNotFoundException()
    assert e1.message == "AudioStream was not found in Polly's response."
    
    e2 = InstitutionNotFoundException()
    assert e2.message == "Institution not found."
