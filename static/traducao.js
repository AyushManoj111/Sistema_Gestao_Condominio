// i18n setup using i18next
;(function () {
  const resources = {
    pt: { translation: {
      title: "Gerente do Condomínio",
      userRole: "Gerente Condomínio",
      logout: "Sair",
      tenants: "Inquilinos",
      houses: "Casas",
      maintenance: "Manutenções",
      contracts: "Contratos",
      parking: "Estacionamento",
      maintenancePending: "Manutenções Pendentes",
      unpaidRent: "Rendas Não Pagas",
      parkingSpots: "Vagas Estacionamento",
      chartTenants: "Inquilinos últimos 6 meses",
      recentMaintenance: "Manutenções Recentes",
      maintenanceExample1: "Canalização: O tubo partiu-se",
      maintenanceExample2: "Elétrica: Todas as tomadas da cozinha não têm corrente",
      seeMore: "Ver mais →",
      chartRent: "Rendas Pagas vs Não Pagas",
      paid: "Pago",
      pending: "Pendente",
      // Login
      appNameLogin: "Sistema de Gestão de Condomínio",
      usernamePlaceholder: "Nome de Utilizador",
      passwordPlaceholder: "Senha",
      forgotPassword: "Esqueceu a senha?",
      login: "Acessar",
      languageHint: "Idioma",
      // Common UI
      add: "Adicionar",
      edit: "Editar",
      delete: "Excluir",
      saveChanges: "Salvar Alterações",
      create: "Criar",
      close: "Fechar",
      searchPlaceholder: "Pesquisar...",
      // Inquilinos
      tenantsList: "Lista de Inquilinos",
      addTenant: "Adicionar Novo Inquilino",
      name: "Nome",
      email: "Email",
      contact: "Contacto",
      house: "Casa",
      actions: "Ações",
      addTenantTitle: "Adicionar Novo Inquilino",
      editTenantTitle: "Editar Inquilino",
      personalData: "Dados Pessoais",
      createTenant: "Criar Inquilino",
      // Tenants - Ramo de atividade
      activityBranch: "Ramo de atividade",
      branch: "Ramo",
      selectBranch: "Selecione o ramo",
      trade: "Comércio",
      services: "Serviços",
      // Casas
      manageHouses: "Gerenciar Casas",
      addHouse: "Adicionar Nova Casa",
      houseNumber: "Número da Casa",
      condominium: "Condomínio",
      tenantName: "Nome do Inquilino",
      createHouse: "Criar Casa",
      editHouseTitle: "Editar Casa",
      // Manutenções
      maintenanceList: "Lista de Manutenções",
      addMaintenance: "Adicionar Nova Manutenção",
      code: "Código",
      building: "Edifício",
      dateTime: "Data/Hora",
      type: "Tipo",
      problem: "Problema",
      description: "Descrição",
      company: "Empresa",
      evidences: "Evidências",
      status: "Estado",
      general: "Geral",
      specific: "Específico",
      saveMaintenance: "Salvar Manutenção",
      noEvidence: "Nenhuma evidência disponível",
      requestMaintenance: "Solicitar Nova Manutenção",
      maintenanceCategory: "Categoria de Manutenção",
      equipments: "Equipamentos",
      systems: "Sistemas",
      physicalStructure: "Estrutura Física",
      specificProblem: "Problema Específico",
      detailedDescription: "Descrição Detalhada",
      contractedCompany: "Empresa Contratada",
      attachEvidenceOptional: "Anexar Evidências (Opcional)",
      attachFileOpenCamera: "Anexar Arquivo / Abrir Câmera",
      unit: "Unidade (Casa/Apartamento)",
      affectedComponent: "Componente/Item Afetado",
      locationInUnit: "Local Afetado na Unidade",
      problemDescription: "Descrição do Problema",
      selectBuilding: "Selecione o Edifício",
      selectProblem: "Selecione o Problema",
      selectUnit: "Selecione a Unidade",
      editMaintenanceTitle: "Editar Manutenção",
      // Estacionamento
      parkingTitle: "Parque de Estacionamento",
      freeSpots: "VAGAS LIVRES",
      tenantsWithSpot: "INQUILINOS COM VAGA",
      visitorsToday: "VISITANTES HOJE",
      totalParking: "Lotação Total do Estacionamento",
      detailedParking: "Lotação Detalhada por Pisos",
      assignedSpots: "Vagas Atribuídas aos Inquilinos",
      addCar: "Adicionar Viatura",
      tenantNameCol: "Nome Inquilino",
      apartment: "Apartamento",
      spotsAssigned: "Lugares Atribuídos",
      floor: "Piso",
      occupied: "Ocupado",
      available: "Disponível",
      newCarTitle: "Adicionar Nova Viatura 🚗",
      vehicleType: "Tipo de Viatura",
      tenantOrHouse: "Inquilino / ID da Casa",
      plate: "Matrícula",
      spotNumber: "Nº Vaga",
      registerCar: "Registrar Viatura",
      // Contratos
      contractsList: "Lista de Contratos",
      addContract: "Adicionar Contrato",
      tenant: "Inquilino",
      totalDuration: "Duração Total",
      remainingDuration: "Duração Restante",
      rentValue: "Valor da Renda",
      successContractAdded: "O contrato foi adicionado com sucesso. ✅",
      addContractTitle: "Adicionar Novo Contrato",
      contractDuration: "Duração do Contrato",
      rentAmount: "Valor da Renda",
      createContract: "Criar Contrato",
      editContractTitle: "Editar Contrato"
    }},
    en: { translation: {
      title: "Condominium Manager",
      userRole: "Condominium Manager",
      logout: "Logout",
      tenants: "Tenants",
      houses: "Houses",
      maintenance: "Maintenance",
      contracts: "Contracts",
      parking: "Parking",
      maintenancePending: "Pending Maintenance",
      unpaidRent: "Unpaid Rent",
      parkingSpots: "Parking Spots",
      chartTenants: "Tenants Last 6 Months",
      recentMaintenance: "Recent Maintenance",
      maintenanceExample1: "Plumbing: The pipe broke",
      maintenanceExample2: "Electrical: All kitchen outlets have no power",
      seeMore: "See more →",
      chartRent: "Paid vs Unpaid Rent",
      paid: "Paid",
      pending: "Pending",
      // Login
      appNameLogin: "Condominium Management System",
      usernamePlaceholder: "Username",
      passwordPlaceholder: "Password",
      forgotPassword: "Forgot password?",
      login: "Sign in",
      languageHint: "Language",
      // Common UI
      add: "Add",
      edit: "Edit",
      delete: "Delete",
      saveChanges: "Save Changes",
      create: "Create",
      close: "Close",
      searchPlaceholder: "Search...",
      // Tenants
      tenantsList: "Tenants List",
      addTenant: "Add New Tenant",
      name: "Name",
      email: "Email",
      contact: "Contact",
      house: "House",
      actions: "Actions",
      addTenantTitle: "Add New Tenant",
      editTenantTitle: "Edit Tenant",
      personalData: "Personal Data",
      createTenant: "Create Tenant",
      // Tenants - Activity Branch
      activityBranch: "Activity Branch",
      branch: "Branch",
      selectBranch: "Select branch",
      trade: "Trade",
      services: "Services",
      // Houses
      manageHouses: "Manage Houses",
      addHouse: "Add New House",
      houseNumber: "House Number",
      condominium: "Condominium",
      tenantName: "Tenant Name",
      createHouse: "Create House",
      editHouseTitle: "Edit House",
      // Maintenance
      maintenanceList: "Maintenance List",
      addMaintenance: "Add New Maintenance",
      code: "Code",
      building: "Building",
      dateTime: "Date/Time",
      type: "Type",
      problem: "Problem",
      description: "Description",
      company: "Company",
      evidences: "Evidence",
      status: "Status",
      general: "General",
      specific: "Specific",
      saveMaintenance: "Save Maintenance",
      noEvidence: "No evidence available",
      requestMaintenance: "Request New Maintenance",
      maintenanceCategory: "Maintenance Category",
      equipments: "Equipment",
      systems: "Systems",
      physicalStructure: "Physical Structure",
      specificProblem: "Specific Problem",
      detailedDescription: "Detailed Description",
      contractedCompany: "Contracted Company",
      attachEvidenceOptional: "Attach Evidence (Optional)",
      attachFileOpenCamera: "Attach File / Open Camera",
      unit: "Unit (House/Apartment)",
      affectedComponent: "Affected Component/Item",
      locationInUnit: "Location in Unit",
      problemDescription: "Problem Description",
      selectBuilding: "Select Building",
      selectProblem: "Select Problem",
      selectUnit: "Select Unit",
      editMaintenanceTitle: "Edit Maintenance",
      // Parking
      parkingTitle: "Parking Lot",
      freeSpots: "FREE SPOTS",
      tenantsWithSpot: "TENANTS WITH SPOT",
      visitorsToday: "VISITORS TODAY",
      totalParking: "Total Parking Occupancy",
      detailedParking: "Detailed Occupancy by Floor",
      assignedSpots: "Assigned Spots to Tenants",
      addCar: "Add Vehicle",
      tenantNameCol: "Tenant Name",
      apartment: "Apartment",
      spotsAssigned: "Assigned Spots",
      floor: "Floor",
      occupied: "Occupied",
      available: "Available",
      newCarTitle: "Add New Vehicle 🚗",
      vehicleType: "Vehicle Type",
      tenantOrHouse: "Tenant / House ID",
      plate: "License Plate",
      spotNumber: "Spot No.",
      registerCar: "Register Vehicle",
      // Contracts
      contractsList: "Contracts List",
      addContract: "Add Contract",
      tenant: "Tenant",
      totalDuration: "Total Duration",
      remainingDuration: "Remaining Duration",
      rentValue: "Rent Amount",
      successContractAdded: "Contract added successfully. ✅",
      addContractTitle: "Add New Contract",
      contractDuration: "Contract Duration",
      rentAmount: "Rent Amount",
      createContract: "Create Contract",
      editContractTitle: "Edit Contract"
    }}
  }

  function setAttrFromKey(selector, attr, dataAttr) {
    document.querySelectorAll(selector).forEach(el => {
      const key = el.getAttribute(dataAttr)
      if (!key) return
      const value = i18next.t(key)
      if (value) el.setAttribute(attr, value)
    })
  }

  function renderTranslations() {
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n')
      const value = i18next.t(key)
      if (value) el.textContent = value
    })
    // Attributes
    setAttrFromKey('[data-i18n-title]', 'title', 'data-i18n-title')
    setAttrFromKey('[data-i18n-placeholder]', 'placeholder', 'data-i18n-placeholder')
    setAttrFromKey('[data-i18n-aria-label]', 'aria-label', 'data-i18n-aria-label')
    const btn = document.getElementById('langToggle')
    if (btn) {
      const lang = i18next.language
      btn.textContent = lang.toUpperCase()
      btn.setAttribute('title', lang === 'pt' ? 'Mudar para EN' : 'Switch to PT')
    }
    if (typeof window.updateCharts === 'function') {
      window.updateCharts(i18next.language)
    }
  }

  function changeLanguage(lang) {
    i18next.changeLanguage(lang).then(() => {
      localStorage.setItem('language', lang)
      renderTranslations()
    })
  }

  function toggleLanguage() {
    const next = (i18next.language || 'pt') === 'pt' ? 'en' : 'pt'
    changeLanguage(next)
  }

  function attachLangToggle() {
    const btn = document.getElementById('langToggle')
    if (btn && !btn.dataset.bound) {
      btn.addEventListener('click', toggleLanguage)
      btn.dataset.bound = 'true'
    }
  }

  window.initI18n = function initI18n() {
    const saved = localStorage.getItem('language') || 'pt'
    if (!window.i18next) return
    i18next.init({ lng: saved, fallbackLng: 'pt', resources }).then(() => {
      renderTranslations()
      attachLangToggle()
    })
  }

  window.renderTranslations = renderTranslations
  window.changeLanguage = changeLanguage
  window.toggleLanguage = toggleLanguage
  window.attachLangToggle = attachLangToggle
})()


