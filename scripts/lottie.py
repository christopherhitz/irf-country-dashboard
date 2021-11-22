def get_icons():
    '''Set the paths to the animated icons, which you want to use in the dash cards header.'''
    url_coonections = "https://assets9.lottiefiles.com/packages/lf20_svy4ivvy.json"
    url_companies = "https://assets1.lottiefiles.com/packages/lf20_wvpdxivl.json"
    url_msg_in = "https://assets1.lottiefiles.com/packages/lf20_ZXgMbf.json"
    url_msg_out = "https://assets9.lottiefiles.com/packages/lf20_yvrh9cry.json"
    url_reactions = "https://assets5.lottiefiles.com/private_files/lf30_y94njU.json"
    options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))
    
    return url_coonections, url_companies, url_msg_in, url_msg_out, url_reactions, options